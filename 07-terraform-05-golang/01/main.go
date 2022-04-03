package main

import "fmt"

func main() {
    fmt.Print("Введите количество метров: ")
    var input float64
    fmt.Scanf("%f", &input)

    output := input * 3.2808

    fmt.Println(input, "m =", output, "ft")    
}