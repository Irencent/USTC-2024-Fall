#include "gendat.h"


void get_dc_table(unsigned int *dc_size,unsigned int *dc_code)
{
	long int i,j,l,k;
	unsigned char tmp;
	char filename[20];
	int val;
	FILE *dcfile;
	int sizenum[16],sizeval[12];
	
	for(i=0;i<12;i++)  sizeval[i]=0;
	
	strcpy(filename,"dc.tab");
	dcfile=fopen(filename,"rb");
	
	if(dcfile==NULL) {
		cout<<"Error!";
		exit(0);
	}

	fseek(dcfile,0,0);
	for(i=0;i<16;i++){
		fread(&tmp,1,1,dcfile);
		val=(int)tmp;
		sizenum[i]=val;
	}
	for(i=0;i<12;i++){
		fread(&tmp,1,1,dcfile);
		val=(int)tmp;
		sizeval[i]=val;
	}

	sizenum[0]=0;
	for(i=1;i<16;i++) sizenum[i]=sizenum[i]+sizenum[i-1];
	for(i=0;i<12;i++){
		j=0;
		while(j<12 && sizeval[j]!=i)
			j++;
		j++;
		if(j>12)
			dc_size[i]=0;
		else{
			for(k=0;sizenum[k]<j;k++) ;
			dc_size[i]=k+1;
		}
    }

	long int code,precode;
	code=-1;i=0;j=0;
	do{
		for(;j<sizenum[i];j++){
			dc_code[sizeval[j]]=code+1;
			code++;
		}
		i++;
		code=(code++)<<1;
    }while(i<16);
	
	fclose(dcfile);
}

//procedure get_ac_table()
//Input parameter : ac_size[256],ac_code[256]
//To give the values of ac_size[256],ac_code[256] form file "dc.tab"
void get_ac_table(unsigned int ac_size[],unsigned int ac_code[])
{
	long int i,j,l,k;
	unsigned char tmp;
	char filename[20];
	int handle,val;
	double length;
	FILE *acfile;
	int sizenum[16],sizeval[256];

	for(i=0;i<256;i++){
		sizeval[i]=0;
		ac_size[i]=ac_code[i]=0xffff;
	}

	strcpy(filename,"ac.tab");
	acfile=fopen(filename,"rb");

	if(acfile==NULL){
		cout<<"Error!";
		exit(0);
	}
	handle = open(filename, O_RDONLY);
	length=filelength(handle);

	fseek(acfile,0,0);
	for(i=0;i<16;i++){
		fread(&tmp,1,1,acfile);
		val=(int)tmp;
		sizenum[i]=val;
	}
	for(i=0;i<length-16;i++){
		fread(&tmp,1,1,acfile);
		val=(int)tmp;
		sizeval[i]=val;
	}

	sizenum[0]=0;
	for(i=1;i<16;i++)
		sizenum[i]=sizenum[i]+sizenum[i-1];
	for(i=0;i<256;i++){
		j=0;
		while(j<=255 && sizeval[j]!=i)
			j++;
		j++;
		if(j>256)
			ac_size[i]=0;
		else{
			for(k=0;sizenum[k]<j;k++) ;
			ac_size[i]=k+1;
		}
    }

	long int code,precode;
	code=-1;i=0;j=0;
	do{
		for(;j<sizenum[i];j++){
			ac_code[sizeval[j]]=code+1;
			code++;
		}
		i++;
		code=(code++)<<1;
    }while(i<16);

	fclose(acfile);
}


void dct(long double buffer[8][8],long double cm[8][8],long double cn[8][8])
{
	double tmp[8][8];
	int i,j,k;
	for(i=0;i<=7;i++)
		for(j=0;j<=7;j++){
			tmp[i][j]=0;
			for(k=0;k<=7;k++)
				tmp[i][j]=tmp[i][j]+cm[i][k]*buffer[k][j];
		}
		for(i=0;i<=7;i++)
			for(j=0;j<=7;j++){
				buffer[i][j]=0;
				for(k=0;k<=7;k++)
					buffer[i][j]=buffer[i][j]+tmp[i][k]*cn[j][k];
			}
}

void idct(long double buffer[8][8],long double cm[8][8],long double cn[8][8])
{
	long double tmp[8][8];
	int i,j,k;
	for(i=0;i<=7;i++)
		for(j=0;j<=7;j++){
			tmp[i][j]=0;
			for(k=0;k<=7;k++)
				tmp[i][j]=tmp[i][j]+cm[k][i]*buffer[k][j];
		}
		for(i=0;i<=7;i++)
			for(j=0;j<=7;j++){
				buffer[i][j]=0;
				for(k=0;k<=7;k++)
					buffer[i][j]=buffer[i][j]+tmp[i][k]*cn[k][j];
				if(buffer[i][j]>127)
					buffer[i][j]=127;
			}
}

void scan(long double cof[64],long double buffer[8][8],int pot_x[64],int pot_y[64])
{
	int i;
	for(i=0;i<=63;i++)
		cof[i]=buffer[pot_x[i]][pot_y[i]];
}

void quan(long double buffer[8][8],long double Q_matrix[8][8])
{
	int i,j;double tmp;
	for(i=0;i<=7;i++)
		for(j=0;j<=7;j++){
			tmp=buffer[i][j]/Q_matrix[i][j];
			if(tmp<0)
				buffer[i][j]=(int)(tmp-0.5);
			else if(tmp>0)
				buffer[i][j]=(int)(tmp+0.5);
			else
				buffer[i][j]=(int)(tmp);
		}
}

void iquan(long double buffer[8][8],long double Q_matrix[8][8])
{
	int i,j;
	for(i=0;i<=7;i++)
		for(j=0;j<=7;j++)
			buffer[i][j]=buffer[i][j]*Q_matrix[i][j];
}




//*stream
//totallen is the data length in current stream
//val is the value to write to the stream
void write(FILE *stream,long int &totallen,unsigned int &val)
{
	unsigned char tmp;
	tmp=(unsigned char)(val>>8);
	fwrite(&tmp,1,1,stream);
	if(tmp==0xff){
		tmp=0;
		fwrite(&tmp,1,1,stream);totallen+=1;
	}
	tmp=(unsigned char)(val&0x00ff);
	fwrite(&tmp,1,1,stream);
	if(tmp==0xff){
		tmp=0;
		fwrite(&tmp,1,1,stream);totallen+=1;
	}
}


void writeend(FILE *stream,long int &totallen,unsigned int &sbuf,int &buflen)
{
	if(buflen<16){
		write(stream,totallen,sbuf);
		totallen+=2;
	}
}

int bit_dc(int &val)
{
	int tmp=fabs(val);
	if (tmp==0)    return 0;
	else if(tmp==1)   return 1;
	else if(tmp<4)    return 2;
	else if(tmp<8)    return 3;
	else if(tmp<16)   return 4;
	else if(tmp<32)   return 5;
	else if(tmp<64)   return 6;
	else if(tmp<128)  return 7;
	else if(tmp<256)  return 8;
	else if(tmp<512)  return 9;
	else if(tmp<1024) return 10;
	else{
		val=val/tmp*2047;
		return 11;
	}
}

int bit_ac(int &val)
{
	int tmp=fabs(val);
	if (tmp==0)    return 0;
	else if(tmp==1)        return 1;
	else if(tmp<4)    return 2;
	else if(tmp<8)    return 3;
	else if(tmp<16)   return 4;
	else if(tmp<32)   return 5;
	else if(tmp<64)   return 6;
	else if(tmp<128)  return 7;
	else if(tmp<256)  return 8;
	else if(tmp<512)  return 9;
	else{
		val=val/tmp*1023;
		return 10;
	}
}

//stream,totallen,buflen,sbuf
void writetostream(FILE *stream,long int &totallen,int &buflen,unsigned int &sbuf,int bitnum,int code,int ssss,int val)
{
	unsigned int test;
	hi=hi+bitnum+ssss;
	test=code;

	if(buflen>bitnum){
		sbuf=sbuf|(test<<(buflen-bitnum));
		buflen=buflen-bitnum;}
	else{
		sbuf=sbuf|(test>>(bitnum-buflen));
		write(stream,totallen,sbuf);
		totallen=totallen+2;
		sbuf=test<<(16-bitnum+buflen);
		buflen=16-bitnum+buflen;
	}

	if(ssss>0){
		if(val>=0) test=val;
		else{
			code=(abs(val))^(0xffff);
			test=(code<<(16-ssss));
			test=(test>>(16-ssss));
		}
		if(buflen>ssss){
			test=(test<<(buflen-ssss));
			sbuf=sbuf|test;
			buflen=buflen-ssss;
		}
		else{
			sbuf=sbuf|(test>>(ssss-buflen));
			write(stream,totallen,sbuf);
			totallen=totallen+2;
			sbuf=test<<(16-ssss+buflen);
			buflen=16-ssss+buflen;
		}
	}
}

//parameter:ac_size,ac_code,runlength,val
void write_ac(unsigned int *ac_size,unsigned int *ac_code,FILE *stream,long int &totallen,int &buflen,unsigned int &sbuf,int runlength,int val)
{
	unsigned char rrrr,ssss;
	unsigned int code,bitnum;
	rrrr=(unsigned char)runlength;
	ssss=(unsigned int)bit_ac(val);
	code=(rrrr<<4)|ssss;
	bitnum=ac_size[code];
	code=ac_code[code];
	writetostream(stream,totallen,buflen,sbuf,bitnum,code,ssss,val);
}

//parameter:dc_size,dc_code,val
void write_dc(unsigned int *dc_size,unsigned int *dc_code,FILE *stream,long int &totallen,int &buflen,unsigned int &sbuf,int val)
{
	unsigned int code,bitnum,ssss;
	ssss=bit_dc(val);
	code=dc_code[ssss];
	bitnum=dc_size[ssss];
	writetostream(stream,totallen,buflen,sbuf,bitnum,code,ssss,val);
}
