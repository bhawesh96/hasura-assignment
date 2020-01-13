package main
import (
	"fmt"
	"errors"
	"strconv"
)

func main() {
	// initialize variables
	var n, m, i, j int
	var stmnt string
	var multiple_found bool
	var magic_nums[1000] int
	var magic_nums_subs[100] string

	fmt.Println("Please enter the value of N: ")
	fmt.Scan(&n)  // input n

	if n <= 0 {
		panic(errors.New("Value of N should be greater than 0"))
	}

	fmt.Println("Please enter the value of M: ")
	fmt.Scan(&m) //  input m

	if m <= 0 {
		panic(errors.New("Value of M should be greater than 0"))
	}

	for i=0; i<m; i++ {
		fmt.Println("Please enter the magic number:	")
		fmt.Scan(&magic_nums[i]) //  input magic number
		fmt.Println("Please enter the substitute: ")
		fmt.Scan(&magic_nums_subs[i]) //  input corresponding substitute
	}

	for i=1; i<=n; i++ {
		stmnt = ""  // the statement to print
		multiple_found = false  // whether multiple is found or not 
		for j=0; j<m; j++ {
			if i%magic_nums[j] == 0 {
				multiple_found = true
				stmnt = stmnt + magic_nums_subs[j]  // multiple is found, append the substitute
			}
		}
		if multiple_found == false {
			stmnt = strconv.Itoa(i)  // if no multiple found
		}
		fmt.Println(stmnt)
	}

}