/*中国科学技术大学  信息科学技术学院  电子工程与信息科学系  2018*/
/*本科生《多媒体技术》课程实验：Android手机上音频的播放与录制*/

/*
原有《多媒体技术》课程的实验的各个项目都是在Microsoft Visual Studio的Visual C++ 6.0下开发，可以运行在Windows操作系统下。
随着智能手机在诸多场合取代了PC机的作用，我们重新考虑原有课程实验项目设置的合理性。
2018年尝试性将Android下多媒体技术开发的内容放入课程实验。
示例代码仅用于教学，代码中对网络上已有代码引用时做了标注。
cxh@ustc.edu.cn,20181007
*/

/*CXH81007
网上很多录音或播放WAV文件的示例代码都没有给出WaveHeader的定义
* 参考 https://blog.csdn.net/sywjn/article/details/7334171
* */

/*wave 文件一共有四个Chunk组成，其中第三个Chunk可以省略，每个Chunk有标示（ID）,大小（size,就是本Chunk的内容部分长度）,内容三部分组成*/
    /*------------------------------------------------
    |             RIFF WAVE Chunk                  |
    |             ID = 'RIFF'                     |
    |             RiffType = 'WAVE'                |
    ------------------------------------------------
    |             Format Chunk                     |
    |             ID = 'fmt '                      |
    ------------------------------------------------
    |             Fact Chunk(optional)             |
    |             ID = 'fact'                      |
    ------------------------------------------------
    |             Data Chunk                       |
    |             ID = 'data'                      |
    ------------------------------------------------*/

//    typedef struct waveheader
//    {
//        /****RIFF WAVE CHUNK*/
//        unsigned char a[4];//四个字节存放'R','I','F','F'
//        long int b;        //整个文件的长度-8;每个Chunk的size字段，都是表示除了本Chunk的ID和SIZE字段外的长度;
//        unsigned char c[4];//四个字节存放'W','A','V','E'
//        /****Format CHUNK*/
//        unsigned char d[4];//四个字节存放'f','m','t',''
//        long int e;       //16后没有附加消息，18后有附加消息；一般为16，其他格式转来的话为18
//        short int f;       //编码方式，一般为0x0001;
//        short int g;       //声道数目，1单声道，2双声道;
//        long int h;        //采样频率;
//        long int i;        //每秒所需字节数;
//        short int j;       //每个采样需要多少字节，若声道是双，则两个一起考虑;
//        short int k;       //即量化位数
//        /***Data Chunk**/
//        unsigned char p[4];//四个字节存放'd','a','t','a'
//        long int q;        //语音数据部分长度，不包括文件头的任何部分
//    } waveheader;//定义WAVE文件的文件头结构体

package cn.edu.ustc.eeis.audiorecorder.wavTools;

import java.io.ByteArrayOutputStream;
import java.io.IOException;

public class WaveHeader {
	public final char fileID[] = { 'R', 'I', 'F', 'F' };
	public int fileLength;
	public char wavTag[] = { 'W', 'A', 'V', 'E' };;
	public char FmtHdrID[] = { 'f', 'm', 't', ' ' };
	public int FmtHdrLeth;
	public short FormatTag;
	public short Channels;
	public int SamplesPerSec;
	public int AvgBytesPerSec;
	public short BlockAlign;
	public short BitsPerSample;
	public char DataHdrID[] = { 'd', 'a', 't', 'a' };
	public int DataHdrLeth;

	public byte[] getHeader() throws IOException {
		ByteArrayOutputStream bos = new ByteArrayOutputStream();
		writeChar(bos, fileID);
		writeInt(bos, fileLength);
		writeChar(bos, wavTag);
		writeChar(bos, FmtHdrID);
		writeInt(bos, FmtHdrLeth);
		writeShort(bos, FormatTag);
		writeShort(bos, Channels);
		writeInt(bos, SamplesPerSec);
		writeInt(bos, AvgBytesPerSec);
		writeShort(bos, BlockAlign);
		writeShort(bos, BitsPerSample);
		writeChar(bos, DataHdrID);
		writeInt(bos, DataHdrLeth);
		bos.flush();
		byte[] r = bos.toByteArray();
		bos.close();
		return r;
	}

	private void writeShort(ByteArrayOutputStream bos, int s) throws IOException {
		byte[] mybyte = new byte[2];
		mybyte[1] = (byte) ((s << 16) >> 24);
		mybyte[0] = (byte) ((s << 24) >> 24);
		bos.write(mybyte);
	}

	private void writeInt(ByteArrayOutputStream bos, int n) throws IOException {
		byte[] buf = new byte[4];
		buf[3] = (byte) (n >> 24);
		buf[2] = (byte) ((n << 8) >> 24);
		buf[1] = (byte) ((n << 16) >> 24);
		buf[0] = (byte) ((n << 24) >> 24);
		bos.write(buf);
	}

	private void writeChar(ByteArrayOutputStream bos, char[] id) {
		for (int i = 0; i < id.length; i++) {
			char c = id[i];
			bos.write(c);
		}
	}
}
