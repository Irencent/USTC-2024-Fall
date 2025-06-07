#define pi 3.1415926
#include <iostream.h>
#include <math.h>
#include <io.h>
#include <stdio.h>
#include <conio.h>
#include <stdlib.h>
#include <graphics.h>
#include <string.h>
#include <fcntl.h>
#define BUF  unsigned long int

double cof[64],buffer[8][8],cm[8][8],cn[8][8],predc;
double  Q_matrix[8][8]={{16,11,10,16,24,40,51,61},
			     {12,12,14,19,26,58,60,55},
			     {14,13,16,24,40,57,69,56},
			     {14,17,22,29,51,87,80,62},
			     {18,22,37,56,68,109,103,77},
			     {24,35,55,64,81,104,113,92},
			     {49,64,78,87,103,121,120,101},
			     {72,92,95,98,112,100,103,99}};

const int pot_x[64]={0,0,1,2,1,0,0,1,2,3,4,3,2,1,0,0,1,2,3,4,5,6,5,4,3,2,1,0,0,1,2,3,4,5,6,7,7,
    6,5,4,3,2,1,2,3,4,5,6,7,7,6,5,4,3,4,5,6,7,7,6,5,6,7,7};
const int  pot_y[64]={0,1,0,0,1,2,3,2,1,0,0,1,2,3,4,5,4,3,2,1,0,0,1,2,3,4,5,6,7,6,5,4,3,2,1,0,1,
    2,3,4,5,6,7,7,6,5,4,3,2,3,4,5,6,7,7,6,5,4,5,6,7,7,6,7};
unsigned char huge trans[256][256];
unsigned int read();
void idct();
void decode();
FILE *outfp,*stream;
char infile[20];
const long int width=256,height=256;
unsigned int dc_size[12],dc_code[12],ac_size[256],ac_code[256];
void get_ac_table(),get_dc_table();
int buflen=0;
BUF rbuf=0;
int readfromstream(int);
int restore_ac(int&,int&);int restore_dc();
int bit_ac(int);int bit_dc(int);
unsigned char search_dc(int );unsigned char search_ac(int );
long int byteposition=0;


void init()
{int i,j;
 FILE *istream;
 unsigned char tmp;

  for(j=0;j<=7;j++)
	{cm[0][j]=sqrt(2)/2/2;
	 cn[0][j]=sqrt(2)/2/2;
	}
  for (i=1;i<=7;i++)
    for (j=0;j<=7;j++)
	 {cm[i][j]=cosl(pi*i*(2*j+1)/16)/2;
	  cn[i][j]=cosl(pi*i*(2*j+1)/16)/2;
	  }

      char filen[20];
      cout<<"Please input the name of datastream file:";
      cin>>filen;
      stream=fopen(filen,"rb");
      if(stream==NULL)
	   {cout<<"File Open Error!";
	    exit(0);}
      fseek(stream,0,0);
      strcpy(filen,"wp.tmp");
      istream=fopen(filen,"wb");
      if(istream==NULL)
	   {cout<<"Tempory File Open Error!";
	    exit(0);}
      fseek(istream,0,0);
      while(!feof(stream))
       {fread(&tmp,1,1,stream);
	fwrite(&tmp,1,1,istream);
	if(tmp==0xff)
	  {fread(&tmp,1,1,stream);
	   if(tmp!=0x00)
	      fwrite(&tmp,1,1,istream);
	   }
	}
     fclose(istream);
     fclose(stream);
     stream=fopen("wp.tmp","rb");
     fseek(stream,0,0);
}

void idct()
{long double tmp[8][8];
 int i,j,k;
 for(i=0;i<=7;i++)
       for(j=0;j<=7;j++)
	  {tmp[i][j]=0;
	   for(k=0;k<=7;k++)
		  tmp[i][j]=tmp[i][j]+cm[k][i]*buffer[k][j];
	   }
 for(i=0;i<=7;i++)
       for(j=0;j<=7;j++)
	  {buffer[i][j]=128;
	   for(k=0;k<=7;k++)
	     buffer[i][j]=buffer[i][j]+tmp[i][k]*cn[k][j];
	   if(buffer[i][j]>255)
		       buffer[i][j]=255;
	   }
}


void iquan()
{int i,j;
 for(i=0;i<=7;i++)
       for(j=0;j<=7;j++)
	      buffer[i][j]=buffer[i][j]*Q_matrix[i][j];
}

void iscan()
{int i,j;
 for(i=0;i<=63;i++)
	buffer[pot_x[i]][pot_y[i]]=cof[i];
}

void get_ac_table()
{int i,j,l,k;
 unsigned char tmp;
 char filename[20];
 int handle,val;
 double length;
 FILE *acfile;
 int sizenum[16],sizeval[256];

 for(i=0;i<256;i++)
   {sizeval[i]=0;
    ac_code[i]=0xffff;}

// cout<<"Please input the filename of AC_Table:";
// cin>>filename;
 strcpy(filename,"ac.tab");
 acfile=fopen(filename,"rb");

 if(acfile==NULL)
   {cout<<"Error!";
    exit(0);}
 handle = open(filename, O_RDONLY);
 length=filelength(handle);

 fseek(acfile,0,0);
 for(i=0;i<16;i++)
    {fread(&tmp,1,1,acfile);
     val=(int)tmp;
     sizenum[i]=val;}
 for(i=0;i<length-16;i++)
    {fread(&tmp,1,1,acfile);
     val=(int)tmp;
     sizeval[i]=val;
     }

 sizenum[0]=0;
 for(i=1;i<16;i++)
     sizenum[i]=sizenum[i]+sizenum[i-1];
 for(i=0;i<256;i++)
   {j=0;
    while(j<=255 && sizeval[j]!=i)
       j++;
    j++;
    if(j>256)
	ac_size[i]=0;
    else
       {for(k=0;sizenum[k]<j;k++) ;
	ac_size[i]=k+1;
	}
    }

 long int code,precode;
 code=-1;i=0;j=0;
 do{
    for(;j<sizenum[i];j++)
     {ac_code[sizeval[j]]=code+1;
      code++;
      }
    i++;
    code=(code++)<<1;
    }while(i<16);
 fclose(acfile);
}

void get_dc_table()
{long int i,j,l,k;
 unsigned char tmp;
 char filename[20];
 int val;
 FILE *dcfile;
 int sizenum[16],sizeval[12];

 for(i=0;i<12;i++)
   sizeval[i]=0;

// cout<<"Please input the filename of AC_Table:";
// cin>>filename;
 strcpy(filename,"dc.tab");
 dcfile=fopen(filename,"rb");

 if(dcfile==NULL)
   {cout<<"Error!";
    exit(0);}

 fseek(dcfile,0,0);
 for(i=0;i<16;i++)
    {fread(&tmp,1,1,dcfile);
     val=(int)tmp;
     sizenum[i]=val;}
 for(i=0;i<12;i++)
    {fread(&tmp,1,1,dcfile);
     val=(int)tmp;
     sizeval[i]=val;
     }

 sizenum[0]=0;
 for(i=1;i<16;i++)
     sizenum[i]=sizenum[i]+sizenum[i-1];
 for(i=0;i<12;i++)
   {j=0;
    while(j<12 && sizeval[j]!=i)
       j++;
    j++;
    if(j>12)
	dc_size[i]=0;
    else
       {for(k=0;sizenum[k]<j;k++) ;
	dc_size[i]=k+1;
	}
    }

 long int code,precode;
 code=-1;i=0;j=0;
 do{
    for(;j<sizenum[i];j++)
     {dc_code[sizeval[j]]=code+1;
      code++;
      }
    i++;
    code=(code++)<<1;
    }while(i<16);
 fclose(dcfile);
}



void main()
{int x; long int i,j,l,k;
 unsigned char gray;
 char tmp[20],flag;
 char filename[20];
 int handle;
 double length;

 init();
 get_ac_table();
 get_dc_table();
 cout<<"waiting......";
 for(i=0;i<(height/8);i++)
   {for(j=0;j<(width/8);j++)
     {decode();
      for(l=0;l<=7;l++)
	for(k=0;k<=7;k++)
	     {gray=(unsigned char)(buffer[l][k]);
	      trans[i*8+l][j*8+k]=(unsigned char)gray;
	      }
      }
    }

 cout<<"Please input the name of output file:";
 cin>>filename;
 outfp=fopen(filename,"wb");
 if(outfp==NULL)
   {cout<<"Error!";
	exit(0);}
 for(i=0;i<256;i++)
   for(j=0;j<256;j++)
     {gray=(unsigned char)trans[i][j];
      fputc(gray,outfp);}
 cout<<byteposition;
 fclose(outfp);
 fclose(stream);
 }


void decode()
{int i,j,k,bak,code;
 int rrrr,ssss,val;

 bak=restore_dc();
 cof[0]=bak+predc;
 predc=cof[0];

 for(i=1;i<=63;)
      {code=restore_ac(rrrr,ssss);
       if((rrrr==0)&&(ssss==0))
	  {for(;i<=63;i++)
	     cof[i]=0;
	   i=64;
	   }
	else
	  {for(j=0;j<rrrr;j++)
	      cof[i+j]=0;
	  i=i+rrrr;
	  cof[i++]=code;
	  }
      }

      iscan();
      iquan();
      idct();
}


int restore_dc()
{int code;
 BUF temp,buf;
 int i,j,ssss,bitnum;
 unsigned int bb;
 if(buflen<16)
     {bb=read();
      temp=bb;
      temp=temp<<16;
      temp=temp>>buflen;
      rbuf=rbuf|temp;
      buflen=buflen+16;}
 for(i=2;i<=9;i++)
    {buf=rbuf>>(32-i);
     for(j=0;dc_size[j]<=i;j++)
	    {if(buf==dc_code[j])
	       {rbuf=rbuf<<i;
		buflen=buflen-i;
		ssss=j;
		code=readfromstream(ssss);
		return code;
		}
	    }
    }
 printf(" decode DC error:\tinvalid buf:%d",rbuf);
 exit(0);
}

int restore_ac(int& rrrr,int& ssss)
{unsigned int code,bb;
 BUF temp;
 BUF buf;
 int i,j,bitnum;
 if(buflen<16)
     {bb=read();
      temp=bb;
      temp=temp<<16;
      temp=temp>>buflen;
      rbuf=rbuf|temp;
      buflen=buflen+16;}
 for(i=2;i<=16;i++)
    {buf=rbuf>>(32-i);
     for(j=0;j<256;j++)
	    {if(buf==ac_code[j])
	       {code=(unsigned char)j;
		rrrr=(code>>4)&0x0f;
		ssss=code&0x000f;
		rbuf=rbuf<<i;
		buflen=buflen-i;
		bb=readfromstream(ssss);
		return bb;}
	    }
    }
 printf(" decode AC error:Invalid buf:%d",rbuf);
 cout<<"\n"<<byteposition;
 getch();
 exit(0);
}

unsigned char search_ac(int code)
{int i;
 for(i=0;i<256;i++)
   if(ac_code[i]==code)
	return ((unsigned char)i);
 cout<<"Decode error:\nnot find"<<code;
 exit(0);
 }

unsigned char search_dc(int code)
{int i;
 for(i=0;i<12;i++)
   if(dc_code[i]==code)
	return i;
 cout<<"Decode error:\nnot find"<<code;
 exit(0);
}

unsigned int read()
{unsigned char temp;
 unsigned int code;
 fread(&temp,1,1,stream);
 code=(unsigned int)temp;
 code=code<<8;
 fread(&temp,1,1,stream);
 code=code|temp;
 byteposition+=2;
 return code;
}


int bit_dc(int val)
{int tmp=fabs(val);
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
 else {val=val/tmp*2047;
       return 11;}
}

int bit_ac(int val)
{int tmp=fabs(val);
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
 else {val=val/tmp*1023;
       return 10;}
}

int readfromstream(int ssss)
{unsigned int code,i;BUF buf;unsigned int test;
 unsigned long int temp;

 if(ssss>11)
    exit(0);
 if(ssss==0)
	    return 0;

 if(buflen<16)
     {temp=read();
      temp=temp<<16;
      temp=temp>>(buflen);
      rbuf=rbuf|temp;
      buflen=buflen+16;}

 buf=rbuf;

 code=(buf>>(32-ssss));
 if(code<pow(2,ssss-1))
      {test=(code^0xffff);
       test=test<<(16-ssss);
       test=test>>(16-ssss);
       code=-abs(test);
       }
      else
	test=code;

 rbuf=rbuf<<ssss;
 buflen=buflen-ssss;

 return code;
}