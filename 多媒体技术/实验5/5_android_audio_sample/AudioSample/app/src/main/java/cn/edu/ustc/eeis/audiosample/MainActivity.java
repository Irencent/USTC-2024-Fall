/*中国科学技术大学  信息科学技术学院  电子工程与信息科学系  2018*/
/*本科生《多媒体技术》课程实验：Android手机上音频的播放与录制*/

/*
原有《多媒体技术》课程的实验的各个项目都是在Microsoft Visual Studio的Visual C++ 6.0下开发，可以运行在Windows操作系统下。
随着智能手机在诸多场合取代了PC机的作用，我们重新考虑原有课程实验项目设置的合理性。
2018年尝试性将Android下多媒体技术开发的内容放入课程实验。
示例代码仅用于教学，代码中对网络上已有代码引用时做了标注。
cxh@ustc.edu.cn,20181007
*/

/*
本程序作为演示Android下多媒体开发的基础函数，在变量声明，代码书写顺序方面尽量按照一个模块相关的变量和函数放在一起的组织方式。
这样方便理解对应的功能模块代码，但是建议同学们在实际编程的时候不要按照这样的方式组织代码！！！
这样方便理解对应的功能模块代码，但是建议同学们在实际编程的时候不要按照这样的方式组织代码！！！
*/
package cn.edu.ustc.eeis.audiosample;

import cn.edu.ustc.eeis.audiosample.wavTools.*;
import android.app.Activity;
import android.graphics.Color;
import android.media.AudioAttributes;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioRecord;
import android.media.AudioTrack;
import android.media.MediaPlayer;
import android.media.MediaRecorder;
import android.media.SoundPool;
import android.os.Bundle;
import android.os.Environment;
import android.os.SystemClock;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.DataOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.text.SimpleDateFormat;
import java.util.Date;

import static android.content.ContentValues.TAG;

public class MainActivity extends Activity implements View.OnClickListener {

    /*CXH20181007：定义界面上5个按钮的访问实例，按钮对应的事件，按钮颜色文字等可以通过这些实例设置或访问 */
    public Button button_play_media_player;
    public Button button_play_sound_pool;
    public Button button_play_audio_track;
    public Button button_audio_record_5s;
    public Button button_start_stop_audio_record_with_thread;

    /*CXH20181007
    * 对象创建完成之后，会执行到该类的onCreate方法，
    * 此onCreate方法是重写父类Activity的onCreate方法而实现的。
    * onCreate方法用来初始化Activity实例对象。
    * 一般情况下我们将自己的初始化代码放置在这个函数内
    * */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        /*播放音频的按钮*/
        button_play_media_player= (Button)findViewById(R.id.button_play_media_player);
        button_play_media_player.setOnClickListener(this);
        button_play_sound_pool= (Button)findViewById(R.id.button_play_sound_pool);
        button_play_sound_pool.setOnClickListener(this);
        button_play_audio_track= (Button)findViewById(R.id.button_play_audio_track);
        button_play_audio_track.setOnClickListener(this);
        /*录音按钮*/
        button_audio_record_5s= (Button)findViewById(R.id.button_audio_record_5s);
        button_audio_record_5s.setOnClickListener(this);
        button_start_stop_audio_record_with_thread= (Button)findViewById(R.id.button_start_stop_audio_record_with_thread);
        button_start_stop_audio_record_with_thread.setOnClickListener(this);

        /*全局变量，gb_isRecordingStart == true，正在录音； gb_isRecordingStart == false，没有在录音*/
        gb_isRecordingStart = false;

    }

    /*CXH20181007
     * 一般情况下我们在onDestroy()中可以做一些清理操作，如资源的释放，指针置空值等
     * */
    @Override
    protected void onDestroy() {
        if (mSoundPool != null) {
            mSoundPool.release();
            mSoundPool = null;
        }
        super.onDestroy();
    }

    /*CXH20181007
    在Android程序中，为控件（按钮）添加监听方式及其处理代码有三种不同的方式
    可参考  https://blog.csdn.net/woniu_manpa/article/details/79417498 学习
    本示例程序中使用的是 在Activity中定义一个内部类继承监听器接口（这里是OnClickListener）
    */
    @Override
    public void onClick(View view) {
        switch(view.getId()){
            /*以下定义各个按钮的响应事件*/
            case R.id.button_play_media_player:
            play_with_media_palyer(Environment.getExternalStorageDirectory().getPath() + "/cxh2018/Ring01.wav");
                break;
            case R.id.button_play_sound_pool:
                play_with_sound_pool(Environment.getExternalStorageDirectory().getPath() + "/cxh2018/Ring02.wav");
                break;
            case R.id.button_play_audio_track:
                play_with_audio_track(Environment.getExternalStorageDirectory().getPath() + "/cxh2018/Ring03.wav");
                break;
            case R.id.button_audio_record_5s:
                audio_record_5s(Environment.getExternalStorageDirectory().getPath() + "/cxh2018/record01.pcm");
                break;
            case R.id.button_start_stop_audio_record_with_thread:
                start_stop_audio_record();
                break;
            default:
                break;
        }
    }

    /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /* CXH20181007：
    可以使用不同的方式进行音乐文件的播放，可参考https://www.cnblogs.com/HDK2016/p/8043247.html  */
    /* 使用MediaPlayer播放本地音乐文件     */
    private MediaPlayer mMediaPlayer = new MediaPlayer();
    void play_with_media_palyer(String str_file_name)
    {
        Toast.makeText(this, str_file_name, Toast.LENGTH_SHORT).show();
        try {
            mMediaPlayer.setDataSource(str_file_name);
            mMediaPlayer.prepare();
            mMediaPlayer.start();
        } catch (IllegalArgumentException e) {
            e.printStackTrace();
        } catch (IllegalStateException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        mMediaPlayer.setOnCompletionListener(new MediaPlayer.OnCompletionListener(){
            @Override
            public void onCompletion(MediaPlayer mMediaPlayer) {
                mMediaPlayer.release();
            }
        });
    }

    /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /* CXH20181007：
    可以使用不同的方式进行音乐文件的播放，可参考https://www.cnblogs.com/HDK2016/p/8043247.html  */
    //使用SoundPool播放本地音乐文件
    private SoundPool mSoundPool;
    int soundID;
    void play_with_sound_pool(String str_file_name)
    {
        Toast.makeText(this, str_file_name, Toast.LENGTH_SHORT).show();
        //设置描述音频流信息的属性
        AudioAttributes abs = new AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_MEDIA)
                .setContentType(AudioAttributes.CONTENT_TYPE_MUSIC)
                .build() ;
        mSoundPool =  new SoundPool.Builder()
                .setMaxStreams(100)   //设置允许同时播放的流的最大值
                .setAudioAttributes(abs)   //完全可以设置为null
                .build() ;
        soundID = mSoundPool.load(str_file_name,1);

        mSoundPool.setOnLoadCompleteListener(new SoundPool.OnLoadCompleteListener() {
            @Override
            public void onLoadComplete(SoundPool soundPool, int sampleId, int status) {
                    mSoundPool.play(soundID, 1.0f, 1.0f, 0, 3,1.0f);
            }
        });
    }

    /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    //使用AudioTrack播放本地音乐文件，WAV文件头格式参见???
    //CXH81006 以下代码参考 https://blog.csdn.net/caiyunfreedom/article/details/6743999
    private AudioTrack player;
    private int audioBufSize;
    private byte[] audioData;
    void play_with_audio_track(String str_file_name) {
        int pcmlen=0;
        Toast.makeText(this, str_file_name, Toast.LENGTH_SHORT).show();
        try {
            FileInputStream fis=new FileInputStream(str_file_name);
            audioData=new byte[1024*1024*2];//2M
            int len=fis.read(audioData);
            Log.i(TAG, "fis len="+len);
            Log.i(TAG, "0:"+(char)audioData[0]);
            pcmlen=0;
            pcmlen+=audioData[0x2b];
            pcmlen=pcmlen*256+audioData[0x2a];
            pcmlen=pcmlen*256+audioData[0x29];
            pcmlen=pcmlen*256+audioData[0x28];
            int channel=audioData[0x17];
            channel=channel*256+audioData[0x16];
            int bits=audioData[0x23];
            bits=bits*256+audioData[0x22];
            Log.i(TAG, "pcmlen="+pcmlen+",channel="+channel+",bits="+bits);
            player = new AudioTrack(AudioManager.STREAM_MUSIC,
                    44100,
                    channel,
                    AudioFormat.ENCODING_PCM_16BIT,
                    pcmlen,
                    AudioTrack.MODE_STATIC);
            player.write(audioData, 0x2C, pcmlen);
            Log.i(TAG, "write 1...");
            player.play();
            Log.i(TAG, "play 1...");
        }
        catch (Exception e) {
            // TODO Auto-generated catch blocke.printStackTrace();
        }

    }


    /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /*CXH81007：将PCM样本文件添加WAV文件的文件头，WAV文件就可以在手机或者PC上用通用的音乐包房软件进行播放了
    代码参考 https://www.jianshu.com/p/90c4071c7768    **/
    /** * 将一个pcm样本文件转化为wav文件 * @param pcmPath pcm文件路径 * @param destinationPath 目标文件路径(wav) * @param deletePcmFile 是否删除源文件 * @return */
    public static boolean makePCMFileToWAVFile(String pcmPath, String destinationPath, boolean deletePcmFile)
    {
        byte buffer[] = null;
        int TOTAL_SIZE = 0;
        File file = new File(pcmPath);
        if (!file.exists())
        {
            return false;
        }
        TOTAL_SIZE = (int) file.length();
        // 填入参数，比特率等等。这里用的是16位单声道 8000 hz
        WaveHeader header = new WaveHeader();
        // 长度字段 = 内容的大小（TOTAL_SIZE) +
        // 头部字段的大小(不包括前面4字节的标识符RIFF以及fileLength本身的4字节)
        header.fileLength = TOTAL_SIZE + (44 - 8);
        header.FmtHdrLeth = 16;
        header.BitsPerSample = 16;
        header.Channels = 2;
        header.FormatTag = 0x0001;
        header.SamplesPerSec = 8000;
        header.BlockAlign = (short) (header.Channels * header.BitsPerSample / 8);
        header.AvgBytesPerSec = header.BlockAlign * header.SamplesPerSec;
        header.DataHdrLeth = TOTAL_SIZE;
        byte[] h = null;
        try {
            h = header.getHeader();
        }
        catch (IOException e1)
        {
            Log.e("PcmToWav", e1.getMessage());
        return false;
        }
        if (h.length != 44)
            // WAV标准，头部应该是44字节,如果不是44个字节则不进行转换文件
            return false;
        // 先删除目标文件
        File destfile = new File(destinationPath);
        if (destfile.exists())
            destfile.delete();
        // 合成的pcm文件的数据，写到目标文件
        try
        {
            buffer = new byte[1024 * 4];
            // Length of All Files, Total Size
            InputStream inStream = null;
            OutputStream ouStream = null;
            ouStream = new BufferedOutputStream(new FileOutputStream( destinationPath));
            ouStream.write(h, 0, h.length);
            inStream = new BufferedInputStream(new FileInputStream(file));
            int size = inStream.read(buffer);
            while (size != -1)
            {
                ouStream.write(buffer);
                size = inStream.read(buffer);
            }
            inStream.close();
            ouStream.close();
        }
        catch (FileNotFoundException e)
        {
            Log.e("PcmToWav", e.getMessage()); return false;
        }
        catch (IOException ioe)
        {
            Log.e("PcmToWav", ioe.getMessage());
            return false;
        }
        if (deletePcmFile)
        {
            file.delete();
        }
        Log.i("PcmToWav", "makePCMFileToWAVFile success!" + new SimpleDateFormat("yyyy-MM-dd hh:mm").format(new Date()));
        return true;
    }


    /////////////////////////////////////////////////////////////////////////////////////////////////////////////

    private AudioRecord mRecorder;
    private DataOutputStream dos;
    private  int bufferSize;
    private boolean isStart = false;

    /*CXH20181007，使用AudioRecord进行录音的简单示例，录音在持续5秒钟后停止，并且自动写入WAV文件
    * 此示例代码仅仅用于演示AudioRecord的关键函数，实际程序中录音功能应该用多线程方式实现
    * */
    void audio_record_5s(String str_file_name)
    {
        long time = SystemClock.uptimeMillis();//记录开始的时间，单位为毫秒
//        Toast.makeText(this, SystemClock.uptimeMillis()- time, Toast.LENGTH_SHORT).show();
        File file = new File(str_file_name);
        try {
            if (file.exists()) {
                file.delete();
            }
            file.createNewFile();
            dos = new DataOutputStream(new FileOutputStream(file, true));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }

        bufferSize = AudioRecord.getMinBufferSize(8000, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT);
        mRecorder = new AudioRecord(MediaRecorder.AudioSource.MIC, 8000, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT, bufferSize * 2);
        mRecorder.startRecording();
        Log.i(TAG, ">>>>mRecorder.startRecording()");
        isStart = true;
        int bytesRecord;
        //int bufferSize = 320;
        byte[] tempBuffer = new byte[bufferSize];

        while (isStart) {
            if((SystemClock.uptimeMillis() - time) > 5000) {//录音时间超过5秒钟自动退出
                isStart = false;
                break;
            }
            if (null != mRecorder) {
                bytesRecord = mRecorder.read(tempBuffer, 0, bufferSize);
                if (bytesRecord == AudioRecord.ERROR_INVALID_OPERATION || bytesRecord == AudioRecord.ERROR_BAD_VALUE) {
                    continue;
                }
                if (bytesRecord != 0 && bytesRecord != -1) {
                    //在此可以对录制音频的数据进行二次处理 比如变声，压缩，降噪，增益等操作
                    //我们这里直接将pcm音频原数据写入文件 这里可以直接发送至服务器 对方采用AudioTrack进行播放原数据
                    try {
                        dos.write(tempBuffer, 0, bytesRecord);
                    } catch (FileNotFoundException e) {
                        e.printStackTrace();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                } else {
                    break;
                }
            }
        }
        mRecorder.stop();
        mRecorder.release();
        Toast.makeText(this, "录音并保存至"+str_file_name, Toast.LENGTH_SHORT).show();
        makePCMFileToWAVFile(Environment.getExternalStorageDirectory().getPath() + "/cxh2018/record01.pcm",
                Environment.getExternalStorageDirectory().getPath() + "/cxh2018/record01.wav",
                false);
    }

    /////////////////////////////////////////////////////////////////////////////////////////////////////////////
    /*CXH20181007 定义使用多线程进行录音控制的类 AudioRecordManager ，此处调用该类，该类参见 AudioRecordManager.java文件*/
    /*全局变量，gb_isRecordingStart == true，正在录音； gb_isRecordingStart == false，没有在录音*/
    private static boolean gb_isRecordingStart = false;
    /*全局变量，AudioRecordManager采用多线程方式启动录音或停止录音，mAudioRecordManager需要在程序不同位置进行访问*/
    AudioRecordManager mAudioRecordManager;
    void start_stop_audio_record() {
        if(gb_isRecordingStart == true) {
            gb_isRecordingStart = false;
            toggle_button(false);
            mAudioRecordManager.stopRecord();
            mAudioRecordManager = null;
            makePCMFileToWAVFile(Environment.getExternalStorageDirectory().getPath() + "/cxh2018/record02.pcm",
                    Environment.getExternalStorageDirectory().getPath() + "/cxh2018/record02.wav",
                    false);
        }
        else{
            gb_isRecordingStart = true;
            toggle_button(true);
            mAudioRecordManager = new AudioRecordManager();
            mAudioRecordManager.startRecord(Environment.getExternalStorageDirectory().getPath() + "/cxh2018/record02.pcm");
        }
    }

    /*控制界面上按钮的颜色和文字做切换*/
    void toggle_button(boolean b_isRecording){
        if(b_isRecording) {
            Toast.makeText(this, "开始录音...", Toast.LENGTH_SHORT).show();
            button_start_stop_audio_record_with_thread.setBackgroundColor(Color.argb(0xFF, 0x9F, 0, 0));
            button_start_stop_audio_record_with_thread.setText("停止录音");
        }
        else
        {
            button_start_stop_audio_record_with_thread.setBackgroundColor(Color.argb(0xFF, 0x4F, 0x8f, 0x8f));
            button_start_stop_audio_record_with_thread.setText("录音（多线程）");
            Toast.makeText(this, "录音已结束", Toast.LENGTH_SHORT).show();
        }
    }
}
