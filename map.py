import matplotlib.pyplot as plt
from japanmap import picture
import base64
from flask import Flask, render_template
import io
import matplotlib

# ... your existing Flask application code ...

app = Flask(__name__)
matplotlib.use("Agg")


# Function to display the Japan map with colored prefectures
def show_japan_map(pref_colors):
    plt.figure(figsize=(8, 8))
    plt.imshow(picture(pref_colors))  # Create the map with colored prefectures
    plt.axis("off")  # Hide axes for a cleaner map view
    plt.title("Japan")

    # Convert the plot to a byte array for image display in Flask
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode("utf-8")

    return img_base64  # Return the Base64-encoded image data


# ... your existing routes ...


@app.route("/map", methods=["GET"])
def show_map():
    # Define prefectures and their colors (example)
    pref_colors = {"北海道": "Blue"}

    # Generate the map image and encode it in Base64
    map_image_data = show_japan_map(pref_colors)

    return render_template("map.html", image_data=map_image_data)  # Pass the image data to the template


# ... your remaining routes ...

if __name__ == "__main__":
    app.run(port=8000, debug=True)
