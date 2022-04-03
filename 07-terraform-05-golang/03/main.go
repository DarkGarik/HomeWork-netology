package main

import (
	"fmt"
	//"strings"
)
func main() {
	all := []string{}
	for i := 1; i <= 100; i++ {
		fmt.Println(i)
		if i%3 == 0{
			all = append(all, string(i))
			fmt.Println(string(i))
		}
	}
	fmt.Println(all)
}