package detector

import (
	_ "net/http/pprof"
	"testing"
)

func TestValueDetect(t *testing.T) {
	DataC := make([]float64, 361)
	for index := range DataC {
		DataC[index] = 1
	}
	DataB := DataC

	DataA := make([]float64, 180)
	for index := range DataA {
		DataA[index] = 1
	}
	DataA = append(DataA, 10)

	isOk, prob := ValueDetect(Sample{
		DataA: DataA,
		DataB: DataB,
		DataC: DataC,
	})
	t.Logf("value detect prob:%f", prob)
	if isOk || prob == 1 || prob < 0 {
		t.Fail()
	}
}

func TestRateDetect(t *testing.T) {
	DataC := make([]float64, 361)
	for index := range DataC {
		DataC[index] = 1
	}
	DataB := DataC

	DataA := make([]float64, 180)
	for index := range DataA {
		DataA[index] = 1
	}
	DataA = append(DataA, 10)

	isOk, prob := RateDetect(Sample{
		DataA: DataA,
		DataB: DataB,
		DataC: DataC,
	})
	t.Logf("rate detect prob:%f", prob)
	if isOk || prob != 0 {
		t.Fail()
	}
}
