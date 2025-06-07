package cn.edu.ustc.eeis.tensorflowandroid;
/*中国科学技术大学  信息科学技术学院  电子工程与信息科学系  2018*/
/*本科生《多媒体技术》课程实验：Android手机上使用tensorflow模型*/

/*
原有《多媒体技术》课程的实验的各个项目都是在Microsoft Visual Studio的Visual C++ 6.0下开发，可以运行在Windows操作系统下。
随着智能手机在诸多场合取代了PC机的作用，我们重新考虑原有课程实验项目设置的合理性。
        2018年尝试性将Android下多媒体技术开发的内容放入课程实验。
        示例代码仅用于教学，代码中对网络上已有代码引用时做了标注。
        cxh@ustc.edu.cn,20181022

本实验项目代码取自
https://blog.csdn.net/guyuealian/article/details/79672257
将tensorflow训练好的模型移植到Android (MNIST手写数字识别)
在此感谢博客专家 pan_jinquan 的分享，希望同学们通过对本例程的学习掌握在Android使用tensorflow模型的基本方法

根据该博文描述的步骤和提供的GitHub代码：https://github.com/PanJinquan/Mnist-tensorFlow-AndroidDemo
略微修改界面，放置了3张测试图片，使用tensorflow所得到模型进行分类，
除了原博文作者提供的图片外，另外2张图片均未能正确识别。

*/
/*
由于Android SDK版本更新，上述2018年的示例代码的编译环境搭建较为困难，故抽取核心代码后再新Android Studio版本下重新设计了示例
    Android Studio Koala Feature Drop | 2024.1.2
    Build #AI-241.18034.62.2412.12266719, built on August 23, 2024
（1）由于Goolgle目前主推的是Kotlin来写gradle，build.gradle改为build.gradle.kts。
    事实上，如果Gradle用java语法，Android Studio图形化向导生成的代码都无法正常编译。
（2）删除了此前示例中关于本地调用C代码的部分（未起作用的代码）
cxh@ustc.edu.cn,20241006
*/

import android.os.Bundle;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    //CXH20241007,删除了此前示例中关于本地调用C代码的部分（未起作用的代码）
    // Used to load the 'native-lib' library on application startup.
    //static {
    //    System.loadLibrary("native-lib");
    //}

    private static final String TAG = "MainActivity";
    // MODEL_FILE 模型存放路径，对应实际的路径为 Mnist-tensorFlow-AndroidDemo-master\app\src\main\assets
    private static final String MODEL_FILE = "file:///android_asset/mnist.pb";
    TextView txt;
    TextView tv;
    ImageView imageView;//用于显示图片
    Bitmap bitmap;//用于读取测试图片
    PredictionTF preTF;//类提供了一个利用已经训练好的tensoflow库进行测试图片preidiction的接口
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // Example of a call to a native method
        tv = (TextView) findViewById(R.id.sample_text);
        txt=(TextView)findViewById(R.id.txt_id);
        imageView =(ImageView)findViewById(R.id.imageView1);
        bitmap = BitmapFactory.decodeResource(getResources(), R.drawable.test_image2);
        imageView.setImageBitmap(bitmap);
        //PredictionTF 构造函数中指定了所需要使用的tensorflow模型函数
        preTF =new PredictionTF(getAssets(),MODEL_FILE);//输入模型存放路径，并加载TensoFlow模型
    }

    //原博客作者提供的测试代码
    public void click02(View v){
        String res="预测结果为：";
        //PredictionTF.PredictionTF()利用训练好的TensoFlow模型预测结果，输入为图片，输出为数字
        int[] result= preTF.getPredict(bitmap);
        for (int i=0;i<result.length;i++){
            Log.i(TAG, res+result[i] );
            res=res+String.valueOf(result[i])+" ";
        }
        txt.setText(res);
        tv.setText(res);
        //CXH20241007,删除了此前示例中关于本地调用C代码的部分（未起作用的代码）
        //tv.setText(stringFromJNI());
    }

    //为了使 click07() 中使用到的变量更加清晰，把变量定义放在 click07() 前面，
    //请同学们注意编程的时候不要用这种风格！！！
    Bitmap bitmap7;//用于读取测试图片
    PredictionTF preTF7;//类提供了一个利用已经训练好的tensoflow库进行测试图片preidiction的接口
    //根据原博客作者提供的测试代码改写，测试另外一个图片
    public void click07(View v){
        bitmap7 = BitmapFactory.decodeResource(getResources(), R.drawable.test_image7);
        imageView.setImageBitmap(bitmap7);
        preTF7 =new PredictionTF(getAssets(),MODEL_FILE);//输入模型存放路径，并加载TensoFlow模型

        String res="预测结果为：";
        //PredictionTF.PredictionTF()利用训练好的TensoFlow模型预测结果，输入为图片，输出为数字
        int[] result= preTF.getPredict(bitmap7);
        for (int i=0;i<result.length;i++){
            Log.i(TAG, res+result[i] );
            res=res+String.valueOf(result[i])+" ";
        }
        txt.setText(res);
        tv.setText(res);
        //CXH20241007,删除了此前示例中关于本地调用C代码的部分（未起作用的代码）
        //tv.setText(stringFromJNI());
    }

    //为了使 click08() 中使用到的变量更加清晰，把变量定义放在 click08() 前面，
    //请同学们注意编程的时候不要用这种风格！！！
    Bitmap bitmap8;//用于读取测试图片
    PredictionTF preTF8;//类提供了一个利用已经训练好的tensoflow库进行测试图片preidiction的接口
    //根据原博客作者提供的测试代码改写，测试另外一个图片
    public void click08(View v){
        bitmap8 = BitmapFactory.decodeResource(getResources(), R.drawable.test_image8);
        imageView.setImageBitmap(bitmap8);
        preTF8 =new PredictionTF(getAssets(),MODEL_FILE);//输入模型存放路径，并加载TensoFlow模型

        String res="预测结果为：";
        //PredictionTF.PredictionTF()利用训练好的TensoFlow模型预测结果，输入为图片，输出为数字
        int[] result= preTF.getPredict(bitmap8);
        for (int i=0;i<result.length;i++){
            Log.i(TAG, res+result[i] );
            res=res+String.valueOf(result[i])+" ";
        }
        txt.setText(res);
        tv.setText(res);
        //CXH20241007,删除了此前示例中关于本地调用C代码的部分（未起作用的代码）
        //tv.setText(stringFromJNI());
    }
    /**
     * A native method that is implemented by the 'native-lib' native library,
     * which is packaged with this application.
     */
    //public native String stringFromJNI();
    // CXH20241007,删除了此前示例中关于本地调用C代码的部分（未起作用的代码）
}
