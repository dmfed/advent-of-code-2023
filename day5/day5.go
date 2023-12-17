package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

const MaxInt = int((^uint(0) >> 1))

type Range struct {
	dst int
	src int
	len int
}

func (r Range) Map(n int) (int, bool) {
	if n < r.src || n > (r.src+r.len-1) {
		return 0, false
	}
	return r.dst - r.src + n, true
}

type Map struct {
	name   string
	ranges []Range
}

func (m *Map) Append(r Range) {
	m.ranges = append(m.ranges, r)
}

func (m *Map) Map(n int) int {
	for i := range m.ranges {
		x, ok := m.ranges[i].Map(n)
		if ok {
			return x
		}
	}
	return n
}

type Almanac struct {
	seeds []int
	maps  []*Map
}

func (a *Almanac) ParseFile(name string) error {
	f, err := os.Open(name)
	if err != nil {
		return err
	}
	defer f.Close()
	scanner := bufio.NewScanner(f)
	scanner.Scan()
	seedsStr := scanner.Text()
	seeds := strToInts(seedsStr[7:])
	a.seeds = seeds
	scanner.Scan()
	var m *Map
	for scanner.Scan() {
		s := scanner.Text()
		s = strings.Trim(s, " \n")
		if s == "" {
			a.maps = append(a.maps, m)
			continue
		}
		if s[0] > '9' {
			m = &Map{
				name:   s,
				ranges: []Range{},
			}
			continue
		}
		nums := strToInts(s)
		r := Range{
			dst: nums[0],
			src: nums[1],
			len: nums[2],
		}
		m.Append(r)
	}
	a.maps = append(a.maps, m)
	return nil
}

func (a *Almanac) seedToLoc(n int) int {
	for i := range a.maps {
		n = a.maps[i].Map(n)
	}
	return n
}

func (a *Almanac) ClosestForSeeds() int {
	result := MaxInt
	for _, n := range a.seeds {
		loc := a.seedToLoc(n)
		if loc < result {
			result = loc
		}
	}
	return result
}

func (a *Almanac) ClosestForRanges() int {
	result := MaxInt
	for i := 0; i < (len(a.seeds) - 2); i += 2 {
		for j := a.seeds[i]; j < (a.seeds[i] + a.seeds[i+1]); j++ {
			loc := a.seedToLoc(j)
			if loc < result {
				result = loc
			}
		}
	}
	return result
}

func strToInts(s string) []int {
	s = strings.Trim(s, " \n")
	split := strings.Split(s, " ")
	nums := []int{}
	for _, x := range split {
		n, err := strconv.Atoi(x)
		if err != nil {
			panic(err)
		}
		nums = append(nums, n)
	}
	return nums
}

func main() {
	a := new(Almanac)
	a.ParseFile("input.txt")

	x := a.ClosestForSeeds()
	fmt.Println(x)

	y := a.ClosestForRanges()
	fmt.Println(y)
}
