package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os/exec"
)

type Source struct {
	TargetType string `json:"target_type"`
	Uri        string `json:"uri"`
}

type Request struct {
	Sources []Source `json:"sources"`
}

type Result struct {
	Source
	Confidence float32 `json:"confidence"`
	Encoding   string  `json:"encoding"`
	Converted  string  `json:"converted"`
}

type Response struct {
	Results []Result `json:"results"`
}

func detect(sources []Source) []Result {
	j, _ := json.Marshal(Request{sources})
	cmd := exec.Command("python", "../pgced.py", string(j))
	var out bytes.Buffer
	cmd.Stdout = &out
	cmd.Run()

	var res Response
	json.Unmarshal([]byte(out.String()), &res)
	return res.Results
}

func main() {
	results := detect([]Source{
		Source{"file", "../test/resource/eucjp"},
		Source{"file", "/home/motoki/ru.txt"},
	})

	for _, result := range results {
		fmt.Printf("%+v\n", result.Encoding)
		fmt.Printf("%+v\n", result.Converted)
	}
}
