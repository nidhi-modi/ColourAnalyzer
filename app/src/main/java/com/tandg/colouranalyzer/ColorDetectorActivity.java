package com.tandg.colouranalyzer;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Color;
import android.graphics.drawable.Drawable;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.LayerDrawable;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.text.SimpleDateFormat;
import java.util.Date;

import butterknife.BindView;
import butterknife.ButterKnife;

public class ColorDetectorActivity extends AppCompatActivity implements View.OnClickListener {

    private static final String TAG = ColorDetectorActivity.class.getSimpleName();

    @BindView(R.id.imgCamera)                   ImageView imgCamera;
    @BindView(R.id.imgGallery)                  ImageView imgGallery;
    @BindView(R.id.imgCircle)                   ImageView imgCircle;
    @BindView(R.id.txtColorName)                TextView txtColorName;
    @BindView(R.id.txtColorNumber)              TextView txtColorNumber;


    String imagePath;
    PyObject pyObject;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_color_detector);

        ButterKnife.bind(this);

        if (! Python.isStarted()) {
            Python.start(new AndroidPlatform(this));
        }


        initResources();
    }

    private void initResources() {

        Python python = Python.getInstance();

        pyObject = python.getModule("colorDetector");


        imgCamera.setOnClickListener(this);
        imgGallery.setOnClickListener(this);

    }

    @Override
    public void onClick(View v) {

        int id = v.getId();
        switch (id){

            case R.id.imgCamera:

                Intent takePicture = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                startActivityForResult(takePicture, 1);



                break;

            case R.id.imgGallery:

                Intent intentGallery = new   Intent(Intent.ACTION_PICK,android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
                startActivityForResult(intentGallery, 2);




                break;
        }


    }

    public String getRealPathFromURI(Uri uri) {
        String path = "";
        if (getContentResolver() != null) {
            Cursor cursor = getContentResolver().query(uri, null, null, null, null);
            if (cursor != null) {
                cursor.moveToFirst();
                int idx = cursor.getColumnIndex(MediaStore.Images.ImageColumns.DATA);
                path = cursor.getString(idx);
                cursor.close();
            }
        }
        return path;
    }

    public Uri getImageUri(Context inContext, Bitmap inImage) {
        ByteArrayOutputStream bytes = new ByteArrayOutputStream();
        inImage.compress(Bitmap.CompressFormat.JPEG, 100, bytes);
        String path = MediaStore.Images.Media.insertImage(inContext.getContentResolver(), inImage, new SimpleDateFormat("yyyyMMddHHmm").format(new Date()), null);
        return Uri.parse(path);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == RESULT_OK) {
            if (requestCode == 1) {
                Bitmap photo = (Bitmap) data.getExtras().get("data");

                // CALL THIS METHOD TO GET THE URI FROM THE BITMAP
                Uri tempUri = getImageUri(getApplicationContext(), photo);
                // CALL THIS METHOD TO GET THE ACTUAL PATH
                File finalFile = new File(getRealPathFromURI(tempUri));

                imagePath = finalFile.getPath();

                Log.e(TAG, "PATH FROM CAMERA: "+finalFile);

                PyObject obj = pyObject.callAttr("processimage",imagePath);

                for (int i = 0; i < obj.asList().size(); i++){

                    Log.e(TAG, "Value of element : "+i + " "+ obj.asList().get(i));

                }



                //testing

                Drawable tempDrawable = getResources().getDrawable(R.drawable.custom_shapes);
                LayerDrawable bubble = (LayerDrawable) tempDrawable;
                GradientDrawable solidColor = (GradientDrawable) bubble.findDrawableByLayerId(R.id.outerRectangle);
                solidColor.setColor(Color.rgb(120,109,60));
                imgCircle.setImageDrawable(tempDrawable);

                //

            } else if (requestCode == 2) {
                Uri selectedImage = data.getData();
                String[] filePath = {MediaStore.Images.Media.DATA};
                Cursor c = getContentResolver().query(selectedImage, filePath, null, null, null);
                c.moveToFirst();
                int columnIndex = c.getColumnIndex(filePath[0]);
                String picturePath = c.getString(columnIndex);
                c.close();
                Bitmap thumbnail = (BitmapFactory.decodeFile(picturePath));

                imagePath = picturePath;

                Log.e(TAG, "PATH FROM GALLERY: "+picturePath);

                PyObject obj2 = pyObject.callAttr("processimage",imagePath);
                for (int i = 0; i < obj2.asList().size(); i++){

                    Log.e(TAG, "Value of element : "+i + " "+ obj2.asList().get(i));

                }
                //viewImage.setImageBitmap(thumbnail);
            }
        }

    }
    }
