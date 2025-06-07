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

package cn.edu.ustc.eeis.audioplayer;

import static android.content.ContentValues.TAG;

import android.app.Activity;
import android.content.pm.PackageManager;
import android.media.AudioAttributes;
import android.media.AudioFormat;
import android.media.AudioManager;
import android.media.AudioTrack;
import android.media.MediaPlayer;
import android.media.SoundPool;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;

import cn.edu.ustc.eeis.audioplayer.wavTools.*;



public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    /*CXH20181007：定义界面上5个按钮的访问实例，按钮对应的事件，按钮颜色文字等可以通过这些实例设置或访问 */
    public Button button_play_media_player;
    public Button button_play_sound_pool;
    public Button button_play_audio_track;

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

        //CXH20241005，早期Android只需要在安装的时候请求权限即可，某个SDK版本后（Android 6.0及以上）需要在运行时请求权限
        //  请求运行时权限 Android Developers (google.cn)
        //  https://developer.android.google.cn/training/permissions/requesting?hl=zh-cn
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED)
        {
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.READ_EXTERNAL_STORAGE}, 1);
        } else {
            Toast.makeText(this, "Get Read Permission", Toast.LENGTH_SHORT).show(); // 用户允许读文件权限请求，显示提示消息
        }
        //CXH20241005，早期Android只需要在安装的时候请求权限即可，某个SDK版本后（Android 6.0及以上）需要在运行时请求权限
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED)
        {
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
        } else {
            Toast.makeText(this, "Get Write Permission", Toast.LENGTH_SHORT).show(); // 用户允许读文件权限请求，显示提示消息
        }

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
        // Correct path to the existing WAV file
        String existingFilePath = getExternalFilesDir(null).getAbsolutePath() + "/record01.wav";

        if(view.getId() == R.id.button_play_media_player)
            play_with_media_palyer(existingFilePath);
        else if(view.getId() == R.id.button_play_sound_pool)
            play_with_sound_pool(existingFilePath);
        else if(view.getId() == R.id.button_play_audio_track)
            play_with_audio_track(existingFilePath);


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

}