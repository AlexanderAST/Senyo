package handler

import "github.com/gin-gonic/gin"

func (h *Handler) handleHello(c *gin.Context) {
	c.JSON(200, gin.H{
		"hello": "world",
	})
}
