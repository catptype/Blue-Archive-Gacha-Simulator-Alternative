package models

import (
	"time"
)

// ==============================================================================
// USER & ROLE MODELS
// ==============================================================================

type Role struct {
	ID   uint   `gorm:"primaryKey"`
	Name string `gorm:"type:varchar(20);unique;not null"`
}

func (Role) TableName() string { return "role_table" }

type User struct {
	ID             uint   `gorm:"primaryKey"`
	Username       string `gorm:"type:varchar(20);unique;index;not null"`
	HashedPassword string `gorm:"type:varchar(255);not null"`
	RoleID         uint   `gorm:"not null"`
	Role           Role   `gorm:"foreignKey:RoleID"`
}

func (User) TableName() string { return "user_table" }

// ==============================================================================
// MAIN DATA MODELS
// ==============================================================================

type Version struct {
	ID   uint   `gorm:"primaryKey"`
	Name string `gorm:"type:varchar(20);unique;not null"`
}

func (Version) TableName() string { return "student_version_table" }

type School struct {
	ID        uint   `gorm:"primaryKey"`
	Name      string `gorm:"type:varchar(20);unique;not null"`
	ImageData []byte `gorm:"type:longblob"` // GORM maps []byte to BLOB
}

func (School) TableName() string { return "student_school_table" }

type ImageAsset struct {
	ID           uint   `gorm:"primaryKey"`
	PortraitData []byte `gorm:"type:longblob"`
	ArtworkData  []byte `gorm:"type:longblob"`
	PairHash     string `gorm:"type:varchar(64);unique;not null"`
}

func (ImageAsset) TableName() string { return "image_asset_table" }

type Student struct {
	ID        uint   `gorm:"primaryKey"`
	Name      string `gorm:"type:varchar(20);not null;uniqueIndex:idx_student_version"`
	Rarity    int    `gorm:"not null"`
	IsLimited bool   `gorm:"default:false"`
	VersionID uint   `gorm:"uniqueIndex:idx_student_version"`
	SchoolID  uint
	AssetID   *uint // Pointer makes it nullable

	Version Version    `gorm:"foreignKey:VersionID"`
	School  School     `gorm:"foreignKey:SchoolID"`
	Asset   ImageAsset `gorm:"foreignKey:AssetID"`
}

func (Student) TableName() string { return "student_table" }

type GachaPreset struct {
	ID         uint    `gorm:"primaryKey"`
	Name       string  `gorm:"type:varchar(20);unique;not null"`
	PickupRate float64 `gorm:"type:decimal(4,1);not null"`
	R3Rate     float64 `gorm:"type:decimal(4,1);not null"`
	R2Rate     float64 `gorm:"type:decimal(4,1);not null"`
	R1Rate     float64 `gorm:"type:decimal(4,1);not null"`
}

func (GachaPreset) TableName() string { return "gacha_preset_table" }

type GachaBanner struct {
	ID             uint   `gorm:"primaryKey"`
	ImageData      []byte `gorm:"type:longblob"`
	Name           string `gorm:"type:varchar(20);unique;not null"`
	IncludeLimited bool   `gorm:"default:false"`
	PresetID       *uint
	Preset         GachaPreset `gorm:"foreignKey:PresetID"`

	// Many-to-Many Relationships
	IncludedVersions []Version `gorm:"many2many:banner_version_association;joinForeignKey:BannerID;joinReferences:VersionID"`
	PickupStudents   []Student `gorm:"many2many:banner_pickup_association;joinForeignKey:BannerID;joinReferences:StudentID"`
	ExcludedStudents []Student `gorm:"many2many:banner_exclude_association;joinForeignKey:BannerID;joinReferences:StudentID"`
}

func (GachaBanner) TableName() string { return "gacha_banner_table" }

// ==============================================================================
// TRANSACTION & LOGGING
// ==============================================================================

type GachaTransaction struct {
	ID        uint      `gorm:"primaryKey"`
	CreateOn  time.Time `gorm:"autoCreateTime"` // Replaces DEFAULT_UTC_NOW
	UserID    uint
	BannerID  uint
	StudentID uint

	User    User        `gorm:"foreignKey:UserID"`
	Banner  GachaBanner `gorm:"foreignKey:BannerID"`
	Student Student     `gorm:"foreignKey:StudentID"`
}

func (GachaTransaction) TableName() string { return "gacha_transaction_table" }

type UserInventory struct {
	ID              uint      `gorm:"primaryKey"`
	NumObtained     int       `gorm:"default:1"`
	FirstObtainedOn time.Time `gorm:"autoCreateTime"`
	UserID          uint      `gorm:"uniqueIndex:idx_user_student"`
	StudentID       uint      `gorm:"uniqueIndex:idx_user_student"`

	User    User    `gorm:"foreignKey:UserID"`
	Student Student `gorm:"foreignKey:StudentID"`
}

func (UserInventory) TableName() string { return "user_inventory_table" }

type Achievement struct {
	ID          uint   `gorm:"primaryKey"`
	Name        string `gorm:"type:varchar(255);unique;not null"`
	Description string `gorm:"type:text"`
	ImageData   []byte `gorm:"type:longblob"`
	Category    string `gorm:"type:varchar(20);default:'MILESTONE'"`
	Key         string `gorm:"type:varchar(50);unique;not null"`
}

func (Achievement) TableName() string { return "achievement_table" }

type UnlockAchievement struct {
	ID            uint      `gorm:"primaryKey"`
	UnlockOn      time.Time `gorm:"autoCreateTime"`
	UserID        uint      `gorm:"uniqueIndex:idx_user_achievement"`
	AchievementID uint      `gorm:"uniqueIndex:idx_user_achievement"`

	User        User        `gorm:"foreignKey:UserID"`
	Achievement Achievement `gorm:"foreignKey:AchievementID"`
}

func (UnlockAchievement) TableName() string { return "unlock_achievement_table" }
