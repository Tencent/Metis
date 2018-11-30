package detector

/*
#include <dlfcn.h>
#include <wrapper.h>
#cgo CFLAGS: -I.
#cgo LDFLAGS: -ldl
*/
import "C"

import (
	"unsafe"
)

const LibPath = "../../lib/libdetect.so"
const xgbModelPath = "../../model/xgb_default_model"
const xgbThreshold = 0.15

var mPtr unsafe.Pointer

func init() {
	hd := C.dlopen(C.CString(LibPath), C.RTLD_LAZY)
	if hd == nil {
		panic("dlopen failure")
	}
	loadModel := C.dlsym(hd, C.CString("load_model"))
	valuePredict := C.dlsym(hd, C.CString("value_predict"))
	ratePredict := C.dlsym(hd, C.CString("rate_predict"))
	if loadModel == nil || valuePredict == nil || ratePredict == nil {
		panic("dlsym failure")
	}
	C.setLoadModel(loadModel)
	C.setValuePredict(valuePredict)
	C.setRatePredict(ratePredict)

	ptr := C.callLoadModel(C.CString(xgbModelPath))
	if ptr == nil {
		panic("load_model return NULL")
	}
	mPtr = ptr
}

func ValueDetect(sample Sample) (bool, float64) {
	dataC := make([]C.int, len(sample.WeekAgo6h))
	for index, value := range sample.WeekAgo6h {
		dataC[index] = C.int(value)
	}
	dataB := make([]C.int, len(sample.Yesterday6h))
	for index, value := range sample.Yesterday6h {
		dataB[index] = C.int(value)
	}
	dataA := make([]C.int, len(sample.Last3h))
	for index, value := range sample.Last3h {
		dataA[index] = C.int(value)
	}
	prob := float64(C.callValuePredict(mPtr,
		(*C.int)(unsafe.Pointer(&dataA[0])),
		(*C.int)(unsafe.Pointer(&dataB[0])),
		(*C.int)(unsafe.Pointer(&dataC[0])),
		(C.int)(len(dataA)),
		(C.int)(len(dataB)),
		(C.int)(len(dataC)),
	))
	return prob >= xgbThreshold, prob
}

func RateDetect(sample Sample) (bool, float64) {
	dataC := make([]C.double, len(sample.WeekAgo6h))
	for index, value := range sample.WeekAgo6h {
		dataC[index] = C.double(value)
	}
	dataB := make([]C.double, len(sample.Yesterday6h))
	for index, value := range sample.Yesterday6h {
		dataB[index] = C.double(value)
	}
	dataA := make([]C.double, len(sample.Last3h))
	for index, value := range sample.Last3h {
		dataA[index] = C.double(value)
	}
	prob := float64(C.callRatePredict(
		(*C.double)(unsafe.Pointer(&dataA[0])),
		(*C.double)(unsafe.Pointer(&dataB[0])),
		(*C.double)(unsafe.Pointer(&dataC[0])),
		(C.int)(len(dataA)),
		(C.int)(len(dataB)),
		(C.int)(len(dataC)),
	))
	return prob > 0, prob
}

type Sample struct {
	Last3h      []float64
	Yesterday6h []float64
	WeekAgo6h   []float64
}
