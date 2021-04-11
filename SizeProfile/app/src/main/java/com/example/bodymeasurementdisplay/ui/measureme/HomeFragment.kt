package com.example.bodymeasurementdisplay.ui.measureme

import android.annotation.SuppressLint
import android.app.Activity.RESULT_CANCELED
import android.app.Activity.RESULT_OK
import android.app.AlertDialog
import android.content.DialogInterface
import android.content.Intent
import android.database.Cursor
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ImageView
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.example.bodymeasurementdisplay.R
import com.example.bodymeasurementdisplay.ui.measureme.Model.Measurement


class HomeFragment : Fragment() {

    protected lateinit var root: View
    private var imageView: ImageView? = null

    override fun onCreateView(
            inflater: LayoutInflater,
            container: ViewGroup?,
            savedInstanceState: Bundle?
    ): View? {
        root = inflater.inflate(R.layout.fragment_home, container, false)
        return root
    }

    override fun onViewCreated(itemView: View, savedInstanceState: Bundle?) {
        super.onViewCreated(itemView, savedInstanceState)

        val camera = root.findViewById<Button>(R.id.button)
        imageView = root.findViewById<ImageView>(R.id.my_image)
        camera.setOnClickListener {
            selectImage()
        }

        val instructions = root.findViewById<Button>(R.id.instructions)
        instructions.setOnClickListener {
            getInstructions()
        }

        val mesh = root.findViewById<Button>(R.id.measuremesh)
        mesh.setOnClickListener {
            getMeasurements()
        }

        val measureR = root.findViewById<RecyclerView>(R.id.recycler_view)
        val measurement = arrayListOf<Measurement>()

        measurement.add(Measurement("Height", 00.00))
        measurement.add(Measurement("Weight", 00.00))
        measurement.add(Measurement("chest", 00.00))
        measurement.add(Measurement("hip", 00.00))
        measurement.add(Measurement("waist", 00.00))
        measurement.add(Measurement("thigh", 00.00))
        measurement.add(Measurement("--", 00.00))


        measureR.apply{
            layoutManager = LinearLayoutManager(this@HomeFragment.requireActivity())
            adapter = MeasurementAdapter(measurement)
        }
    }

    private fun selectImage() {
        val options = arrayOf<CharSequence>("Take Photo", "Choose from Gallery", "Cancel")
        val builder: AlertDialog.Builder = AlertDialog.Builder(context)
        builder.setTitle("Choose your picture")
        builder.setItems(options, DialogInterface.OnClickListener { dialog, item ->
            if (options[item] == "Take Photo") {
                val takePicture = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
                startActivityForResult(takePicture, 0)
            } else if (options[item] == "Choose from Gallery") {
                val pickPhoto = Intent(Intent.ACTION_PICK, MediaStore.Images.Media.EXTERNAL_CONTENT_URI)
                startActivityForResult(pickPhoto, 1)
            } else if (options[item] == "Cancel") {
                dialog.dismiss()
            }
        })
        builder.show()

    }

    private fun getInstructions() {
        val builder: AlertDialog.Builder = AlertDialog.Builder(context)
        builder.setTitle("Instructions")
        builder.setMessage("Click a picture with your feat and hands apart. Click on measureme button to get your measurements!")
        builder.show()
    }

    @SuppressLint("NewApi")
    private fun getMeasurements() {
        val builder: AlertDialog.Builder = AlertDialog.Builder(context)
        builder.setView(R.layout.modelgif)
        builder.setTitle("3D mesh")
        builder.show()

        val measureR = root.findViewById<RecyclerView>(R.id.recycler_view)
        val measurement = arrayListOf<Measurement>()

        measurement.add(Measurement("Height", 167.354))
        measurement.add(Measurement("Weight", 83.909))
        measurement.add(Measurement("chest", 83.43))
        measurement.add(Measurement("hip", 71.39))
        measurement.add(Measurement("waist", 66.91))
        measurement.add(Measurement("thigh", 61.18))
        measurement.add(Measurement("--", 00.00))

        measureR.apply{
            layoutManager = LinearLayoutManager(this@HomeFragment.requireActivity())
            adapter = MeasurementAdapter(measurement)
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (resultCode != RESULT_CANCELED) {
            when (requestCode) {
                0 -> if (resultCode == RESULT_OK && data != null) {
                    val selectedImage = data.extras!!["data"] as Bitmap?
                    imageView?.setImageBitmap(selectedImage)
                }
                1 -> if (resultCode == RESULT_OK && data != null) {
                    val selectedImage: Uri? = data.data
                    val filePathColumn = arrayOf(MediaStore.Images.Media.DATA)
                    if (selectedImage != null) {
                        val cursor: Cursor? = activity?.contentResolver?.query(selectedImage,
                                filePathColumn, null, null, null)
                        if (cursor != null) {
                            cursor.moveToFirst()
                            val columnIndex: Int = cursor.getColumnIndex(filePathColumn[0])
                            val picturePath: String = cursor.getString(columnIndex)

                            // Get the dimensions of the View
                            val targetW: Int = imageView!!.width
                            val targetH: Int = imageView!!.height

                            val bmOptions = BitmapFactory.Options().apply {
                                // Get the dimensions of the bitmap
                                inJustDecodeBounds = true
                                BitmapFactory.decodeFile(picturePath, this)

                                val photoW: Int = imageView!!.width
                                val photoH: Int = imageView!!.height

                                // Determine how much to scale down the image
                                val scaleFactor: Int = Math.max(1, Math.min(photoW / targetW, photoH / targetH))

                                // Decode the image file into a Bitmap sized to fill the View
                                inJustDecodeBounds = false
                                inSampleSize = scaleFactor
                                inPurgeable = true
                            }
                            imageView?.setImageBitmap(BitmapFactory.decodeFile(picturePath, bmOptions))

                            cursor.close()
                        }
                    }
                }
            }
        }
    }
}