package main

import "fmt"

func main() {
	all := []int{}
	for i := 1; i <= 100; i++ {
		if i%3 == 0{
			all = append(all, i)
			//fmt.Println(i)
		}
	}
	fmt.Println(all)
}