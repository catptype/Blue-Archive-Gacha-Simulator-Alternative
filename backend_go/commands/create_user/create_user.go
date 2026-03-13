package main

import (
	"flag"
	"fmt"
	"log"

	"backend/models" // Replace 'backend' with your go.mod module name

	"github.com/glebarez/sqlite"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
)

func main() {
	// 1. Setup CLI Arguments (argparse equivalent)
	// Usage: go run cmd/create_user/main.go -u myuser -p mypass -r superuser
	username := flag.String("u", "", "The username for the new user")
	password := flag.String("p", "", "The password for the new user")
	roleName := flag.String("r", "superuser", "The role (member or superuser)")
	flag.Parse()

	// 2. Validation
	if *username == "" || *password == "" {
		fmt.Println("Error: Username and Password are required.")
		fmt.Println("Usage: go run cmd/create_user/main.go -u <name> -p <pass> [-r <role>]")
		return
	}

	// 3. Connect to Database
	db, err := gorm.Open(sqlite.Open("gacha.db"), &gorm.Config{})
	if err != nil {
		log.Fatalf("Failed to connect to database: %v", err)
	}

	fmt.Printf("Attempting to create user '%s' with role '%s'...\n", *username, *roleName)

	// 4. Check if user already exists
	var existing models.User
	result := db.Where("username = ?", *username).Limit(1).Find(&existing)
	if result.RowsAffected > 0 {
		fmt.Printf("Error: User '%s' already exists.\n", *username)
		return
	}

	// 5. Find the Role object
	var role models.Role
	err = db.Where("name = ?", *roleName).First(&role).Error
	if err != nil {
		fmt.Printf("Error: Role '%s' does not exist in the database.\n", *roleName)
		fmt.Println("Please run the seeder first to initialize roles.")
		return
	}

	// 6. Hash the password (get_password_hash equivalent)
	// DefaultCost is a good balance between security and speed
	hashedBytes, err := bcrypt.GenerateFromPassword([]byte(*password), bcrypt.DefaultCost)
	if err != nil {
		log.Fatalf("Failed to hash password: %v", err)
	}
	hashedPassword := string(hashedBytes)

	// 7. Create the User
	newUser := models.User{
		Username:       *username,
		HashedPassword: hashedPassword,
		RoleID:         role.ID,
	}

	if err := db.Create(&newUser).Error; err != nil {
		log.Fatalf("Failed to save user: %v", err)
	}

	fmt.Printf("Successfully created user '%s' with role '%s'.\n", *username, *roleName)
}
