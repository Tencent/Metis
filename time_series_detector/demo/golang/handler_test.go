package detector

import (
	_ "net/http/pprof"
	"testing"
)

func TestValueDetect(t *testing.T) {
	weekAgoData := make([]float64, 361)
	for index := range weekAgoData {
		weekAgoData[index] = 1
	}
	yesterdayData := weekAgoData

	last3hData := make([]float64, 180)
	for index := range last3hData {
		last3hData[index] = 1
	}
	last3hData = append(last3hData, 10)

	isOk, prob := ValueDetect(Sample{
		WeekAgo6h:   weekAgoData,
		Last3h:      last3hData,
		Yesterday6h: yesterdayData,
	})
	t.Logf("value detect prob:%f", prob)
	if isOk || prob == 1 || prob < 0 {
		t.Fail()
	}
}

func TestRateDetect(t *testing.T) {
	weekAgoData := make([]float64, 361)
	for index := range weekAgoData {
		weekAgoData[index] = 1
	}
	yesterdayData := weekAgoData

	last3hData := make([]float64, 180)
	for index := range last3hData {
		last3hData[index] = 1
	}
	last3hData = append(last3hData, 10)

	isOk, prob := RateDetect(Sample{
		WeekAgo6h:   weekAgoData,
		Last3h:      last3hData,
		Yesterday6h: yesterdayData,
	})
	t.Logf("rate detect prob:%f", prob)
	if isOk || prob != 0 {
		t.Fail()
	}
}
