package main

import (
	"fmt"
	"io/ioutil"
	"strings"

	"github.com/hashicorp/hcl"
)

type Terra struct {
	Source  string
	Resouce string
}

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func readDir() []string {
	var list []string
	files, err := ioutil.ReadDir("../tf-s3/")
	check(err)

	for _, f := range files {
		if strings.Contains(f.Name(), ".tf") {
			list = append(list, f.Name())
		}
	}
	return list
}

func main() {
	fileList := readDir()
	for _, file := range fileList {
		fileName := "../tf-s3/" + file
		dat, err := ioutil.ReadFile(fileName)
		check(err)
		var tf Terra
		hcl.Decode(tf, string(dat))
		fmt.Print(tf)

	}
}
