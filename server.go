package senyo

import (
	"fmt"
	"senyo/internal/handler"

	"github.com/spf13/viper"
)

func StartServer() error {
	srv := handler.NewHandler()

	if err := initConfig(); err != nil {
		srv.Logger.Fatalf("cannot start server %s", err)
		return err
	}

	port := viper.GetString("port")

	fmt.Println("Server started")

	return srv.Router.Run(port)
}

func initConfig() error {
	viper.AddConfigPath("configs")
	viper.SetConfigName("config")
	return viper.ReadInConfig()
}
