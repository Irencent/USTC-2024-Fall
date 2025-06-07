plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "cn.edu.ustc.eeis.tensorflowandroid"
    compileSdk = 34

    defaultConfig {
        applicationId = "cn.edu.ustc.eeis.tensorflowandroid"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        ndk {
            abiFilters.addAll(arrayOf("armeabi-v7a"))
        //CXH20241007， 如果要支持64bits的ARMv8a架构，需要找到对应64bits的库
        // （libtensorflow_inference.so，及 libandroid_tensorflow_inference_java.jar）
            //abiFilters.addAll(arrayOf("armeabi-v7a","arm64-v8a"))
        }
        externalNativeBuild {
            cmake {
                cppFlags += ""
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
    buildFeatures {
        viewBinding = true
    }
    //jniLibs目录指向libs目录
    sourceSets {
        getByName("main") {
            jniLibs.srcDirs("libs")
        }
    }

    ndkVersion = "26.1.10909125"
}

dependencies {
    //这里添加libandroid_tensorflow_inference_java.jar包,否则不能解析TensoFlow包
    implementation(files("libs/libandroid_tensorflow_inference_java.jar"))

    implementation(libs.appcompat)
    implementation(libs.material)
    implementation(libs.constraintlayout)
    implementation(libs.lifecycle.livedata.ktx)
    implementation(libs.lifecycle.viewmodel.ktx)
    implementation(libs.navigation.fragment)
    implementation(libs.navigation.ui)
    testImplementation(libs.junit)
    androidTestImplementation(libs.ext.junit)
    androidTestImplementation(libs.espresso.core)
}