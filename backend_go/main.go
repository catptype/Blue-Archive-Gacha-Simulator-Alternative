package main

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	// 1. Initialize Gin router
	r := gin.Default()

	// 2. A simple test route (Like @app.get("/") in FastAPI)
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})

	// 3. Run the server on port 8000
	r.Run(":8000")
}
