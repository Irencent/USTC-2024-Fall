/*中国科学技术大学  信息科学技术学院  电子工程与信息科学系  2018~2024*/
/*本科生《多媒体技术》课程实验：Android手机上音频的播放与录制*/

/*
原有《多媒体技术》课程的实验的各个项目都是在Microsoft Visual Studio的Visual C++ 6.0下开发，可以运行在Windows操作系统下。
随着智能手机在诸多场合取代了PC机的作用，我们重新考虑原有课程实验项目设置的合理性。
2018年尝试性将Android下多媒体技术开发的内容放入课程实验。
示例代码仅用于教学，代码中对网络上已有代码引用时做了标注。
cxh@ustc.edu.cn,20181007
*/
/*
由于Android SDK版本更新，上述2018年的示例代码的编译环境搭建较为困难，故抽取核心代码后再新Android Studio版本下重新设计了示例
    Android Studio Koala Feature Drop | 2024.1.2
    Build #AI-241.18034.62.2412.12266719, built on August 23, 2024
cxh@ustc.edu.cn,20241006
*/

/*
CXH20181007
这个例子基本上反应出使用AudioRecord类进行录音控制的过程，但是声音的样本仅仅保存为RAW格式，如果需要存成WAV文件，需要加文件头
参考 https://blog.csdn.net/u012426327/article/details/77837073
*/
package cn.edu.ustc.eeis.audiorecorder;

import static android.content.ContentValues.TAG;

import android.Manifest;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import android.os.Bundle;
import android.os.Environment;
import android.os.SystemClock;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

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
import java.text.SimpleDateFormat;
import java.util.Date;

import cn.edu.ustc.eeis.audiorecorder.wavTools.*;



public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    /*CXH20181007：定义界面上5个按钮的访问实例，按钮对应的事件，按钮颜色文字等可以通过这些实例设置或访问 */
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

        /*录音按钮*/
        button_audio_record_5s= (Button)findViewById(R.id.button_audio_record_5s);
        button_audio_record_5s.setOnClickListener(this);
        button_start_stop_audio_record_with_thread= (Button)findViewById(R.id.button_start_stop_audio_record_with_thread);
        button_start_stop_audio_record_with_thread.setOnClickListener(this);

        /*全局变量，gb_isRecordingStart == true，正在录音； gb_isRecordingStart == false，没有在录音*/
        gb_isRecordingStart = false;

        //CXH20241005，早期Android只需要在安装的时候请求权限即可，某个SDK版本后（Android 6.0及以上）需要在运行时请求权限
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED)
        {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO}, 1);
        } else {
            Toast.makeText(this, "Get Record Permission", Toast.LENGTH_SHORT).show(); // 用户允许读文件权限请求，显示提示消息
        }

    }

    /*CXH20181007
    在Android程序中，为控件（按钮）添加监听方式及其处理代码有三种不同的方式
    可参考  https://blog.csdn.net/woniu_manpa/article/details/79417498 学习
    本示例程序中使用的是 在Activity中定义一个内部类继承监听器接口（这里是OnClickListener）
    */
    @Override
    public void onClick(View view) {
        if(view.getId() == R.id.button_audio_record_5s) {
            // CXH20241005，在Android 11及以后的版本中，不能再使用WRITE_EXTERNAL_STORAGE获取写文件的权限
            // 本示例重点在于演示录音有关库函数的使用，故改为读写内部文件，内部文件保存路径为：/android/data/cn.edu.ustc.eeis.audiorecorder/
            // 关于不同类型文件读写权限的获得方法，可以参阅 https://developer.android.google.cn/training/data-storage?hl=zh-cn
            //audio_record_5s(Environment.getExternalStorageDirectory().getPath() + "/cxh2024/record01.pcm");
            // Get the public shared directory for music files
            audio_record_5s(getExternalFilesDir(null).getAbsolutePath() + "/record02.wav");
        }
        else if(view.getId() == R.id.button_start_stop_audio_record_with_thread)
            start_stop_audio_record();

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
    private  int mBufferSizeInBytes;
    private boolean isStart = false;

    /*CXH20181007，使用AudioRecord进行录音的简单示例，录音在持续5秒钟后停止，并且自动写入WAV文件
     * 此示例代码仅仅用于演示AudioRecord的关键函数，实际程序中录音功能应该用多线程方式实现
     * */
    void audio_record_5s(String str_file_name)
    {
        long time = SystemClock.uptimeMillis();//记录开始的时间，单位为毫秒
//        Toast.makeText(this, SystemClock.uptimeMillis()- time, Toast.LENGTH_SHORT).show();
        File file = new File(str_file_name);
        //File file = new File(getExternalFilesDir(null).getAbsolutePath() + "/record01.pcm");
        Log.e("lu", "file new");
        try {
            if (file.exists()) {
                Log.e("lu", "file exists");
                file.delete();
            }
            file.createNewFile();
            Log.e("lu", "file create new");
            //dos = new DataOutputStream(new FileOutputStream(file, true));
            //获取到文件的数据流
            dos = new DataOutputStream(new BufferedOutputStream(new FileOutputStream(file, true)));
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        //Toast.makeText(this, str_file_name, Toast.LENGTH_SHORT).show();

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.RECORD_AUDIO}, 1);
            return;
        }
        mBufferSizeInBytes = AudioRecord.getMinBufferSize(8000, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT);
        mRecorder = new AudioRecord(MediaRecorder.AudioSource.MIC, 8000, AudioFormat.CHANNEL_IN_MONO, AudioFormat.ENCODING_PCM_16BIT, mBufferSizeInBytes * 2);
        //判断AudioRecord的状态是否初始化完毕
        //在AudioRecord对象构造完毕之后，就处于AudioRecord.STATE_INITIALIZED状态了。
        if (mRecorder.getState() == AudioRecord.STATE_UNINITIALIZED) {
            throw new RuntimeException("The AudioRecord is not uninitialized");
        }

        isStart = true;
        try {
            byte[] buffer = new byte[mBufferSizeInBytes];
            mRecorder.startRecording();//开始录音
            Log.i(TAG, ">>>>mRecorder.startRecording()");
            //getRecordingState获取当前AudioReroding是否正在采集数据的状态
            while (isStart && mRecorder.getRecordingState() == AudioRecord.RECORDSTATE_RECORDING) {
                if((SystemClock.uptimeMillis() - time) > 5000) {//录音时间超过5秒钟自动退出
                    isStart = false;
                    break;
                }
                int bufferReadResult = mRecorder.read(buffer,0,mBufferSizeInBytes);
                for (int i = 0; i < bufferReadResult; i++)
                {
                    dos.write(buffer[i]);
                }
            }
            dos.close();
        } catch (Throwable t) {
            Log.e("lu", "Recording Failed");
        }

        mRecorder.stop();
        mRecorder.release();
        Toast.makeText(this, "录音并保存至"+getExternalFilesDir(null).getAbsolutePath() , Toast.LENGTH_SHORT).show();
        makePCMFileToWAVFile(str_file_name,
                getExternalFilesDir(null).getAbsolutePath()  + "/record01.wav",
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
// CXH20241005，在Android 11及以后的版本中，不能再使用WRITE_EXTERNAL_STORAGE获取写文件的权限
// 本示例重点在于演示录音有关库函数的使用，故改为读写内部文件，内部文件保存路径为：/android/data/cn.edu.ustc.eeis.audiorecorder/
// 关于不同类型文件读写权限的获得方法，可以参阅 https://developer.android.google.cn/training/data-storage?hl=zh-cn
//            makePCMFileToWAVFile(Environment.getExternalStorageDirectory().getPath() + "/cxh2024/record02.pcm",
//                    Environment.getExternalStorageDirectory().getPath() + "/cxh2024/record02.wav",
//                    false);
            makePCMFileToWAVFile(getExternalFilesDir(null).getAbsolutePath() + "/record02.pcm",
                    getExternalFilesDir(null).getAbsolutePath()+ "/record02.wav",
                    false);
        }
        else{
            gb_isRecordingStart = true;
            toggle_button(true);
            mAudioRecordManager = new AudioRecordManager();
// CXH20241005，在Android 11及以后的版本中，不能再使用WRITE_EXTERNAL_STORAGE获取写文件的权限
// 本示例重点在于演示录音有关库函数的使用，故改为读写内部文件，内部文件保存路径为：/android/data/cn.edu.ustc.eeis.audiorecorder/
// 关于不同类型文件读写权限的获得方法，可以参阅 https://developer.android.google.cn/training/data-storage?hl=zh-cn
//            mAudioRecordManager.startRecord(Environment.getExternalStorageDirectory().getPath() + "/cxh2024/record02.pcm");
            mAudioRecordManager.startRecord(getExternalFilesDir(null).getAbsolutePath() + "/record02.pcm");
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

