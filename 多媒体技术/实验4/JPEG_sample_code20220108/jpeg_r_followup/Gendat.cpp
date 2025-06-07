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
#include "func.cpp"

//FILE *stream,*infp;
const long int width=256,height=256;

void main()
{
	int x; long int i,j,l,k;
	unsigned char gray;
	char tmp[20],flag;
	char filename[20];
	int handle;
	double length;

	init(stream,cm,cn);
	get_ac_table(ac_size,ac_code);
	get_dc_table(dc_size,dc_code);
	/* cout<<"Please input the name of datafile:";
	cin>>infile;*/
	strcpy(infile,"lady.dat");
	infp=fopen(infile,"rb");
	if(infp==NULL){
		cout<<"Error!";
		exit(0);
	}

	unsigned char temp;
	fseek(infp,0,0);
	for(i=0;i<height;i++)
		for(j=0;j<width;j++){
			fread(&temp,1,1,infp);
			source[i][j]=int(temp);
		}

		cout<<"waiting......\n";
		for(i=0;i<height/8;i++){
			for(j=0;j<width/8;j++){
				for(l=0;l<=7;l++)
					for(k=0;k<=7;k++)
						buffer[l][k]=double(source[i*8+l][j*8+k])-128;
					dct(buffer,cm,cn);
					quan(buffer,Q_matrix);
					scan(cof,buffer,pot_x,pot_y);
					encode();
					iquan(buffer,Q_matrix);
					idct(buffer,cm,cn);
			}
		}
		writeend(stream,totallen,sbuf,buflen);

		cout<<"\nresult length = "<<totallen<<"\n"<<hi/8;
		getch();
                cout << "begin close infp";
		fclose(infp);
//		fclose(outfp);
		cout << "begin close stream";
		fclose(stream);
		cout << "end close stream";
		return;
}


void encode()
{
	int runlength=0,bak=cof[0],preval;
	int i,j,last=0;

	for(i=63;i>=0;i--)
		if(int(cof[i])!=0){
			last=i;break;
		}

		cof[0]=cof[0]-predc;
		predc=bak;
		write_dc(dc_size,dc_code,stream,totallen,buflen,sbuf,cof[0]);

		for(i=1;i<=last;i++){
			if(int(cof[i])==0)
				runlength++;
			else{
				write_ac(ac_size,ac_code,stream,totallen,buflen,sbuf,runlength,int(cof[i]));
				runlength=0;
			}
			if(runlength>15){
				write_ac(ac_size,ac_code,stream,totallen,buflen,sbuf,15,0);
				runlength=1;
			}
		}

		if((last<63)&&last>=0)
			write_ac(ac_size,ac_code,stream,totallen,buflen,sbuf,0,0);
}

