package main

import (
	senyo "senyo"

	"github.com/joho/godotenv"
	"github.com/sirupsen/logrus"
)

func main() {
	if err := godotenv.Load(); err != nil {
		logrus.Fatal(err)
	}

	if err := senyo.StartServer(); err != nil {
		logrus.Fatal(err)
	}
}
