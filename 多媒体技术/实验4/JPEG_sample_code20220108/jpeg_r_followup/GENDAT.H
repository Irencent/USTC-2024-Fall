#define pi 3.1415926
#include <iostream.h>
#include <math.h>
#include <io.h>
#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include <string.h>
#include <fcntl.h>
#define BUF  unsigned int

char infile[20];
int predc=0,buflen=16;
/*  buflen indicate the empty count bit of the SBUF;*/
BUF sbuf=0;
long int totallen=0;
double hi=0;
FILE *infp,*stream;


unsigned int dc_size[12],dc_code[12],ac_size[256],ac_code[256];
//Input parameter : ac_size[256],ac_code[256]
void get_ac_table(unsigned int ac_size[],unsigned int ac_code[]);
//Input parameter : dc_size[12],dc_code[12]
void get_dc_table(unsigned int *dc_size,unsigned int *dc_code);

long double cof[64],buffer[8][8],cm[8][8],cn[8][8];
int pot_x[64]={0,0,1,2,1,0,0,1,2,3,4,3,2,1,0,0,1,2,3,4,5,6,5,4,3,2,1,0,0,1,2,3,4,5,6,7,7,
    6,5,4,3,2,1,2,3,4,5,6,7,7,6,5,4,3,4,5,6,7,7,6,5,6,7,7};
int  pot_y[64]={0,1,0,0,1,2,3,2,1,0,0,1,2,3,4,5,4,3,2,1,0,0,1,2,3,4,5,6,7,6,5,4,3,2,1,0,1,
    2,3,4,5,6,7,7,6,5,4,3,2,3,4,5,6,7,7,6,5,4,5,6,7,7,6,7};

//dct() Input parameter : buffer,cm,cn
//根据cm[][]和cn[][]对buffer[][]进行DCT变换
void dct(long double buffer[8][8],long double cm[8][8],long double cn[8][8]);
//idct() Input parameter : buffer,cm,cn
//根据cm[][]和cn[][]对buffer[][]进行IDCT变换
void idct(long double buffer[8][8],long double cm[8][8],long double cn[8][8]);
//scan() Input parameter : cof[64],buffer[8][8],pot_x[64],pot_y[64]
//To give the values of cof[64] from buffer[8][8],pot_x[64],pot_y[64]
//Z将8*8数据块转换为Z型扫描的顺序
void scan(long double cof[64],long double buffer[8][8],int pot_x[64],int pot_y[64]);

long double  Q_matrix[8][8]={{16,11,10,16,24,40,51,61},
			     {12,12,14,19,26,58,60,55},
			     {14,13,16,24,40,57,69,56},
			     {14,17,22,29,51,87,80,62},
			     {18,22,37,56,68,109,103,77},
			     {24,35,55,64,81,104,113,92},
			     {49,64,78,87,103,121,120,101},
			     {72,92,95,98,112,100,103,99}};
//quan() Input parameter : buffer,Q_matrix
//根据q_matrix[][]对buffer[][]进行量化
void quan(long double buffer[8][8],long double Q_matrix[8][8]);
//iquan() Input parameter : buffer,Q_matrix
//根据q_matrix[][]对buffer[][]进行解量化
void iquan(long double buffer[8][8],long double Q_matrix[8][8]);

int huge source[256][256];

void encode();


//Input parameter : stream,cm[8][8],cn[8][8]
//To give the values of cm[8][8],cn[8][8],And create a new file which you input it's filename
//void init(FILE *stream,long double cm[8][8],long double cn[8][8]);

//parameter:ac_size,ac_code,runlength,val
void write_ac(unsigned int *ac_size,unsigned int *ac_code,FILE *stream,long int &totallen,int &buflen,unsigned int &sbuf,int runlength,int val);
void write_dc(unsigned int *dc_size,unsigned int *dc_code,FILE *stream,long int &totallen,int &buflen,unsigned int &sbuf,int val);
//stream,totallen,buflen,sbuf
void writetostream(FILE *stream,long int &totallen,int &buflen,unsigned int &sbuf,int bitnum,int code,int ssss,int val);

int bit_dc(int &);
int bit_ac(int &);

void write(FILE *stream,long int &totallen,unsigned int &val);
//void write1(unsigned char );
void writeend(FILE *stream,long int &totallen,unsigned int &sbuf,int &buflen);
//int getvalue(long int);
