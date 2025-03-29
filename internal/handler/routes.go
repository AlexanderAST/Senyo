package handler

func (h *Handler) initRoutes() {
	h.Router.GET("/hello", h.handleHello)
}