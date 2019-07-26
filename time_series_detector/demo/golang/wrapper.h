#include <stdio.h>
#include <string.h>
#include <stdlib.h>


typedef struct {
    int* data_a;
    int* data_b;
    int* data_c;
    int len_a;
    int len_b;
    int len_c;
} ValueData;

typedef struct {
    double* data_a;
    double* data_b;
    double* data_c;
    int len_a;
    int len_b;
    int len_c;
} RateData;

void * (*load_model)(const char*);
void setLoadModel(void* fn) {
    load_model = fn;
}
void * callLoadModel(const char *fname){
    return load_model(fname);
};

int (*value_predict)(void *, ValueData*, int*, float*);
void setValuePredict(void* fn){
	value_predict = fn;
}
float callValuePredict(void * mhandle, int* data_a, int* data_b, int* data_c, int len_a, int len_b, int len_c){
	int sample_result=0;
	float prob=0;

	ValueData *dt=malloc(sizeof(ValueData));
	dt->data_a = (int*)malloc(sizeof(int)*len_a);
	dt->data_b = (int*)malloc(sizeof(int)*len_b);
	dt->data_c = (int*)malloc(sizeof(int)*len_c);
	memcpy(dt->data_a, data_a, sizeof(int)*len_a);
	memcpy(dt->data_b, data_b, sizeof(int)*len_b);
	memcpy(dt->data_c, data_c, sizeof(int)*len_c);
	dt->len_a = len_a;
	dt->len_b = len_b;
	dt->len_c = len_c;

	value_predict(mhandle, dt, &sample_result,&prob);
	free(dt->data_a);
	free(dt->data_b);
	free(dt->data_c);
	free(dt);
	return prob;
}

int (*rate_predict)(RateData* data, int* sample_result, float* prob);
void setRatePredict(void* fn){
	rate_predict = fn;
}
float callRatePredict(double *data_a, double* data_b, double* data_c, int len_a, int len_b, int len_c){
	int sample_result=0;
	float prob=0;

	RateData *dt= malloc(sizeof(RateData));

	dt->data_a = (double*)malloc(sizeof(double)*len_a);
	dt->data_b = (double*)malloc(sizeof(double)*len_b);
	dt->data_c = (double*)malloc(sizeof(double)*len_c);
	memcpy(dt->data_a, data_a, sizeof(double)*len_a);
	memcpy(dt->data_b, data_b, sizeof(double)*len_b);
	memcpy(dt->data_c, data_c, sizeof(double)*len_c);
	dt->len_a = len_a;
	dt->len_b = len_b;
	dt->len_c = len_c;

	rate_predict(dt, &sample_result, &prob);
	free(dt->data_a);
	free(dt->data_b);
	free(dt->data_c);
	free(dt);
	return prob;
}
