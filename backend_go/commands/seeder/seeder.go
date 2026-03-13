package main

import (
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"sort"

	"backend_go/models" // Adjust this to your actual module name/folder

	// "github.com/glebarez/sqlite"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

// JSON Input Structs (Like Pydantic/DTOs) to match your JSON files
type StudentJSON struct {
	Name      string `json:"name"`
	Version   string `json:"version"`
	School    string `json:"school"`
	Rarity    int    `json:"rarity"`
	IsLimited bool   `json:"is_limited"`
	Base64    struct {
		Portrait string `json:"portrait"`
		Artwork  string `json:"artwork"`
	} `json:"base64"`
}

type SchoolJSON struct {
	Name        string `json:"name"`
	ImageBase64 string `json:"image_base64"`
}

type PresetJSON struct {
	Name   string  `json:"name"`
	Pickup float64 `json:"pickup"`
	R3     float64 `json:"r3"`
	R2     float64 `json:"r2"`
	R1     float64 `json:"r1"`
}

type BannerJSON struct {
	Name    string   `json:"name"`
	Preset  string   `json:"preset"`
	Version []string `json:"version"`
	Pickup  []struct {
		Name    string `json:"name"`
		Version string `json:"version"`
	} `json:"pickup"`
	Limited     bool   `json:"limited"`
	ImageBase64 string `json:"image_base64"`
}

type AchievementJSON struct {
	Key         string `json:"key"`
	Category    string `json:"category"`
	Name        string `json:"name"`
	Description string `json:"description"`
	ImageBase64 string `json:"image_base64"`
}

var dataDir = "data"

func main() {
	// 1. Connect to Database
	db, err := gorm.Open(sqlite.Open("gacha.db"), &gorm.Config{})
	if err != nil {
		// log.Fatal("failed to connect database")
		log.Fatal(err)
	}

	// 2. Auto Migrate (Ensures tables exist)
	fmt.Println("Initializing database tables...")
	db.AutoMigrate(
		&models.Role{}, &models.User{}, &models.Version{},
		&models.School{}, &models.ImageAsset{}, &models.Student{},
		&models.GachaPreset{}, &models.GachaBanner{}, &models.Achievement{},
	)

	// 3. Run Seeders
	seedRoles(db)
	seedVersions(db)
	seedSchools(db)
	seedStudents(db)
	seedPresets(db)
	seedBanners(db)
	seedAchievements(db)

	fmt.Println("\nDatabase seeding complete!")
}

func seedRoles(db *gorm.DB) {
	fmt.Println("Seeding Roles...")
	roles := []string{"superuser", "member"}
	for _, name := range roles {
		var role models.Role
		db.FirstOrCreate(&role, models.Role{Name: name})
	}
}

func seedVersions(db *gorm.DB) {
	fmt.Println("Seeding Versions...")

	// Phase 1: Ensure Original is ID 1
	var original models.Version
	db.FirstOrCreate(&original, models.Version{Name: "Original"})

	// Phase 2: Read from students directory
	files, _ := filepath.Glob(filepath.Join(dataDir, "students", "*.json"))
	versionSet := make(map[string]bool)
	for _, f := range files {
		var s StudentJSON
		content, _ := os.ReadFile(f)
		json.Unmarshal(content, &s)
		if s.Version != "Original" {
			versionSet[s.Version] = true
		}
	}

	var names []string
	for name := range versionSet {
		names = append(names, name)
	}
	sort.Strings(names)

	for _, name := range names {
		db.FirstOrCreate(&models.Version{}, models.Version{Name: name})
	}
}

func seedSchools(db *gorm.DB) {
	fmt.Printf("\nSeeding Schools...\n")
	content, _ := os.ReadFile(filepath.Join(dataDir, "schools.json"))
	var schools []SchoolJSON
	json.Unmarshal(content, &schools)

	for _, s := range schools {
		imgBytes, _ := base64.StdEncoding.DecodeString(s.ImageBase64)
		db.FirstOrCreate(&models.School{}, models.School{
			Name:      s.Name,
			ImageData: imgBytes,
		})
		fmt.Printf("  - Added School: %s\n", s.Name)
	}
}

func seedStudents(db *gorm.DB) {
	fmt.Printf("\nSeeding Students...\n")

	// 1. Get all JSON files in the students folder
	files, _ := filepath.Glob(filepath.Join(dataDir, "students", "*.json"))

	for _, f := range files {
		// 2. Read and Parse JSON
		var sj StudentJSON
		content, err := os.ReadFile(f)
		if err != nil {
			fmt.Printf("Error reading file %s: %v\n", f, err)
			continue
		}
		json.Unmarshal(content, &sj)

		// 3. Find the related Version and School ID
		var version models.Version
		var school models.School
		db.Where("name = ?", sj.Version).First(&version)
		db.Where("name = ?", sj.School).First(&school)

		// 4. CHECK IF STUDENT EXISTS (Using Find to avoid noisy logs)
		var existing models.Student
		result := db.Where("name = ? AND version_id = ?", sj.Name, version.ID).Limit(1).Find(&existing)

		// result.RowsAffected == 0 means the student is NOT in the database yet
		if result.RowsAffected == 0 {
			// 5. Decode Base64 images
			pBytes, _ := base64.StdEncoding.DecodeString(sj.Base64.Portrait)
			aBytes, _ := base64.StdEncoding.DecodeString(sj.Base64.Artwork)

			// 6. Generate Hashes (Same as your Python logic)
			pHash := fmt.Sprintf("%x", sha256.Sum256(pBytes))
			aHash := fmt.Sprintf("%x", sha256.Sum256(aBytes))
			combinedHash := fmt.Sprintf("%x", sha256.Sum256([]byte(pHash+"-"+aHash)))

			// 7. Create the ImageAsset first
			asset := models.ImageAsset{
				PortraitData: pBytes,
				ArtworkData:  aBytes,
				PairHash:     combinedHash,
			}

			// We use db.Create to save to database.
			// asset.ID will be automatically updated after this call.
			db.Create(&asset)

			// 8. Create the Student linked to the asset
			student := models.Student{
				Name:      sj.Name,
				Rarity:    sj.Rarity,
				IsLimited: sj.IsLimited,
				VersionID: version.ID,
				SchoolID:  school.ID,
				AssetID:   &asset.ID, // Link to the asset we just created
			}
			db.Create(&student)

			fmt.Printf("  + Added Student: %s (%s)\n", sj.Name, sj.Version)
		} else {
			fmt.Printf("  X Already Existing Student: %s (%s)\n", sj.Name, sj.Version)
		}
	}
}

func seedPresets(db *gorm.DB) {
	fmt.Printf("\nSeeding Presets...\n")
	content, _ := os.ReadFile(filepath.Join(dataDir, "presets.json"))
	var presets []PresetJSON
	json.Unmarshal(content, &presets)

	for _, p := range presets {
		db.FirstOrCreate(&models.GachaPreset{}, models.GachaPreset{
			Name:       p.Name,
			PickupRate: p.Pickup,
			R3Rate:     p.R3,
			R2Rate:     p.R2,
			R1Rate:     p.R1,
		})
	}
}

func seedBanners(db *gorm.DB) {
	fmt.Printf("\nSeeding Banners...\n")
	files, _ := filepath.Glob(filepath.Join(dataDir, "banners", "*.json"))

	for _, f := range files {
		var bj BannerJSON
		content, _ := os.ReadFile(f)
		json.Unmarshal(content, &bj)

		var count int64
		db.Model(&models.GachaBanner{}).Where("name = ?", bj.Name).Count(&count)
		if count == 0 {
			var preset models.GachaPreset
			db.Where("name = ?", bj.Preset).First(&preset)

			var versions []models.Version
			db.Where("name IN ?", bj.Version).Find(&versions)

			var pickups []models.Student
			for _, p := range bj.Pickup {
				var s models.Student
				db.Joins("Version").Where("student_table.name = ? AND Version.name = ?", p.Name, p.Version).First(&s)
				pickups = append(pickups, s)
			}

			imgBytes, _ := base64.StdEncoding.DecodeString(bj.ImageBase64)
			banner := models.GachaBanner{
				Name:             bj.Name,
				ImageData:        imgBytes,
				IncludeLimited:   bj.Limited,
				PresetID:         &preset.ID,
				IncludedVersions: versions,
				PickupStudents:   pickups,
			}
			db.Create(&banner)
			fmt.Printf("  - Added Banner: %s\n", bj.Name)
		}
	}
}

func seedAchievements(db *gorm.DB) {
	fmt.Printf("\nSeeding Achievements...\n")

	// 1. Find all JSON files in the achievements directory
	files, _ := filepath.Glob(filepath.Join(dataDir, "achievements", "*.json"))

	for _, f := range files {
		// 2. Read file
		content, err := os.ReadFile(f)
		if err != nil {
			fmt.Printf("  - Error reading file %s: %v\n", f, err)
			continue
		}

		// 3. Parse JSON
		var aj AchievementJSON
		json.Unmarshal(content, &aj)

		// 4. Validate key (Requirement from your Python script)
		if aj.Key == "" {
			fmt.Printf("  - SKIPPING achievement file %s: Missing required 'key'\n", f)
			continue
		}

		// 5. Check if achievement exists (Using Find to keep logs clean)
		var existing models.Achievement
		result := db.Where("key = ?", aj.Key).Limit(1).Find(&existing)

		if result.RowsAffected == 0 {
			// 6. Handle Defaults (Same logic as your Python script)
			category := aj.Category
			if category == "" {
				category = "MILESTONE"
			}

			name := aj.Name
			if name == "" {
				name = "Unnamed Achievement"
			}

			// 7. Decode Image if exists
			var imgBytes []byte
			if aj.ImageBase64 != "" {
				imgBytes, _ = base64.StdEncoding.DecodeString(aj.ImageBase64)
			}

			// 8. Create the Record
			newAchievement := models.Achievement{
				Key:         aj.Key,
				Category:    category,
				Name:        name,
				Description: aj.Description,
				ImageData:   imgBytes,
			}

			if err := db.Create(&newAchievement).Error; err != nil {
				fmt.Printf("  - Error saving achievement %s: %v\n", name, err)
			} else {
				fmt.Printf("  + Added Achievement: %s\n", name)
			}
		}
	}
}
