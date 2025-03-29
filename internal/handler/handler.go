package handler

import (
	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

type Handler struct {
	Router *gin.Engine
	Logger *logrus.Logger
}

func NewHandler() *Handler {
	h := &Handler{
		Router: gin.Default(),
		Logger: logrus.New(),
	}

	h.initRoutes()

	return h
}
