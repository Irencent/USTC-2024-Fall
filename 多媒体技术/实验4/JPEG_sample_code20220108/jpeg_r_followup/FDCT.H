#ifndef DCT_H
#define DCT_H
#include <math.h>
#define ROOT 1.41421356
const double PI=3.1415926536;


void idct(double a[8][8],double b[8][8])
 {
  double g1,g2,g3,g4,t,t1,t2,c[8][8];
  int i,j,k,l,x0,y0,scale;
  for (i=0;i<8;i++)
	for (j=0;j<8;j++)
		b[i][j]=a[i][j];
  for (i=0;i<8;i++)
	{
	 b[i][0]/=ROOT;
	 b[0][i]/=ROOT;
	}
  scale=8;
  for (i=0;i<3;i++)
	{
	 x0=0;
	 y0=0;
	 scale/=2;
	 for (j=0;j<(1<<(2*i));j++)
		{
		 for(k=0;k<scale;k++)
			for(l=0;l<scale;l++)
				{
				 c[x0+k][y0+l]=b[x0+2*k][y0+2*l];
				 c[x0+scale+k][y0+l]=b[x0+2*k+1][y0+2*l]+(k==0?
0:b[x0+2*k-1][y0+2*l]);
				 c[x0+k][y0+scale+l]=b[x0+2*k][y0+2*l+1]+(l==0?
0:b[x0+2*k][y0+2*l-1]);
				 c[x0+scale+k][y0+scale+l]=b[x0+2*k+1][y0+2*l+1]+
(k==0?0:b[x0+2*k-1][y0+2*l+1])+(l==0?0:b[x0+2*k+1][y0+2*l-1])
+(k==0||l==0?0:b[x0+2*k-1][y0+2*l-1]);
				}
		 x0+=scale*2;
		 if(x0>=8)
			{
			 x0=0;
			 y0+=scale*2;
			}
		 for(k=0;k<8;k++)
			for(l=0;l<8;l++)
				b[k][l]=c[k][l];
	 }
  }
 t=PI/4;
 for(i=0;i<3;i++)
  {
   x0=0;
   y0=0;
   for(j=0;j<(1<<(4-2*i));j++)
	{
	 for(k=0;k<scale;k++)
	   {
		t1=2*cos((2*k+1)*t);
		for(l=0;l<scale;l++)
			{
			 t2=2*cos((2*l+1)*t);
			 g1=b[x0+k][y0+l];
			 g2=b[x0+k][y0+scale+l]/t2;
			 g3=b[x0+scale+k][y0+l]/t1;
			 g4=b[x0+scale+k][y0+scale+l]/(t1*t2);
			 c[x0+k][y0+l]=g1+g2+g3+g4;
			 c[x0+k][y0+2*scale-1-l]=g1-g2+g3-g4;
			 c[x0+2*scale-1-k][y0+l]=g1+g2-g3-g4;
			 c[x0+2*scale-1-k][y0+2*scale-1-l]=g1-g2-g3+g4;
			}
	   }
	 x0+=scale*2;
	 if(x0>=8)
		{
		 x0=0;
		 y0+=scale*2;
		}
	 for(k=0;k<8;k++)
		for(l=0;l<8;l++)
			b[k][l]=c[k][l];
	}
   scale*=2;
   t/=2;
  }
 }

void dct(double a[8][8],double b[8][8])
 {
  double p,q,r,s,t,t1,t2,c[8][8];
  int i,j,k,l,x0,y0,scale;
  for (i=0;i<8;i++)
	for (j=0;j<8;j++)
		b[i][j]=a[i][j];
  scale=8;
  t=PI/32;
  for (i=0;i<3;i++)
	{
	 x0=0;
	 y0=0;
	 scale/=2;
	 t*=2;
	 for (j=0;j<(1<<(2*i));j++)
		{
		 for(k=0;k<scale;k++)
		  {
			t1=2*cos((2*k+1)*t);
			for(l=0;l<scale;l++)
				{
				 t2=2*cos((2*l+1)*t);
				 p=b[x0+k][y0+l];
				 q=b[x0+k][y0+2*scale-1-l];
				 r=b[x0+2*scale-1-k][y0+l];
				 s=b[x0+2*scale-1-k][y0+2*scale-1-l];
				 c[x0+k][y0+l]=p+q+r+s;
				 c[x0+k][y0+scale+l]=(p-q+r-s)/t2;
				 c[x0+scale+k][y0+l]=(p+q-r-s)/t1;
				 c[x0+scale+k][y0+scale+l]=(p-q-r+s)/(t1*t2);
				}
		   }
		 x0+=scale*2;
		 if(x0>=8)
			{
			 x0=0;
			 y0+=scale*2;
			}
		 for(k=0;k<8;k++)
			for(l=0;l<8;l++)
				b[k][l]=c[k][l];
	 }
  }
  for(i=0;i<3;i++)
   {
	x0=0;
	y0=0;
	for(j=0;j<(1<<(4-2*i));j++)
	 {
	  for(k=0;k<scale;k++)
		for(l=0;l<scale;l++)
			{
			 c[x0+2*k][y0+2*l]=b[x0+k][y0+l];
			 c[x0+2*k][y0+2*l+1]=b[x0+k][y0+scale+l]+
		(l+1==scale?0:b[x0+k][y0+scale+l+1]);
			 c[x0+2*k+1][y0+2*l]=b[x0+scale+k][y0+l]+
		(k+1==scale?0:b[x0+scale+k+1][y0+l]);
			 c[x0+2*k+1][y0+2*l+1]=b[x0+scale+k][y0+scale+l]+
		(k+1==scale?0:b[x0+scale+k+1][y0+scale+l])+
		(l+1==scale?0:b[x0+scale+k][y0+scale+l+1])+
		(k+1==scale||l+1==scale?0:b[x0+scale+k+1][y0+scale+l+1]);
			}
	 x0+=scale*2;
	 if(x0>=8)
		{
		 x0=0;
		 y0+=scale*2;
		}
	 for(k=0;k<8;k++)
		for(l=0;l<8;l++)
			b[k][l]=c[k][l];
	}
   scale*=2;
  }
  for (i=0;i<8;i++)
	{
	 b[i][0]/=ROOT/4;
	 b[0][i]/=ROOT/4;
	 for (j=0;j<8;j++)
		 b[i][j]/=4;
	}
 }
#endif



