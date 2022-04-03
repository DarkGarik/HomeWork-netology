package main

import "fmt"

func main() {
	x := []int{48,96,86,68,57,82,63,70,37,34,83,27,19,97,9,17,}
	min := 1<<63 - 1
	for _, numbers := range x {
		if numbers < min {
			min = numbers
		}
	}
	fmt.Println(min, "минимальное число в списке:", x)
}