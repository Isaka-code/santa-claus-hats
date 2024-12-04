import os

import streamlit as st
from PIL import Image

# サンタクロースの帽子画像のパス
SANTA_HAT_PATH = "assets/santa_hat.png"
OUTPUT_DIR = "outputs"


# ディレクトリの準備
def prepare_directories():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


# サンタクロースの帽子をプロフィール画像に合成する関数
def add_santa_hat(
    profile_image: Image.Image,
    santa_hat: Image.Image,
    hat_scale: float,
    hat_offset_x: int,
    hat_offset_y: int,
    hat_rotation: int,
) -> Image.Image:
    """
    プロフィール画像にサンタクロースの帽子を重ねる。

    Parameters:
        profile_image (Image.Image): ユーザーがアップロードしたプロフィール画像。
        santa_hat (Image.Image): サンタクロースの帽子画像。
        hat_scale (float): 帽子のサイズを調整するスケール。
        hat_offset_x (int): 帽子の横方向のオフセット。
        hat_offset_y (int): 帽子の縦方向のオフセット。
        hat_rotation (int): 帽子の回転角度。

    Returns:
        Image.Image: 合成された画像。
    """
    profile_image = profile_image.convert("RGBA")
    santa_hat = santa_hat.convert("RGBA")

    # 帽子のサイズをプロフィール画像に合わせて調整
    hat_width = int(profile_image.width * hat_scale)
    hat_height = int(santa_hat.height * (hat_width / santa_hat.width))
    santa_hat = santa_hat.resize((hat_width, hat_height), Image.Resampling.LANCZOS)

    # 帽子を回転
    santa_hat = santa_hat.rotate(hat_rotation, expand=True)

    # 帽子の位置（中央に配置し、オフセットを適用）
    hat_position = (
        (profile_image.width - santa_hat.width) // 2
        + hat_offset_x,  # 中央揃え + 横方向オフセット
        hat_offset_y,  # 縦方向のオフセット
    )

    # 画像を合成
    combined_image = Image.alpha_composite(
        profile_image, Image.new("RGBA", profile_image.size, (0, 0, 0, 0))
    )
    combined_image.paste(santa_hat, hat_position, santa_hat)

    return combined_image


# Streamlitアプリ
def main():
    st.title("サンタプロフィール画像メーカー")

    # サンタ帽子のロード
    try:
        santa_hat = Image.open(SANTA_HAT_PATH)
    except FileNotFoundError:
        st.error(
            "サンタクロースの帽子画像が見つかりません！assetsディレクトリにsanta_hat.pngを配置してください。"
        )
        return

    # プロフィール画像のアップロード
    uploaded_file = st.file_uploader(
        "プロフィール画像をアップロードしてください", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        profile_image = Image.open(uploaded_file)

        # 帽子のサイズ、位置、回転を調整するスライダー
        hat_scale = st.slider(
            "帽子のサイズ (画像幅に対する割合)",
            min_value=0.1,
            max_value=1.0,
            value=0.6,
            step=0.05,
        )
        hat_offset_x = st.slider(
            "帽子の横方向位置調整",
            min_value=-profile_image.width,
            max_value=profile_image.width,
            value=0,
            step=5,
        )
        hat_offset_y = st.slider(
            "帽子の縦方向位置調整",
            min_value=-profile_image.height,
            max_value=profile_image.height,
            value=-10,
            step=5,
        )
        hat_rotation = st.slider(
            "帽子の回転角度 (度)", min_value=-180, max_value=180, value=0, step=5
        )

        # サンタクロースの帽子を合成
        combined_image = add_santa_hat(
            profile_image,
            santa_hat,
            hat_scale,
            hat_offset_x,
            hat_offset_y,
            hat_rotation,
        )

        # 合成画像を表示
        st.image(
            combined_image,
            caption="サンタクロースプロフィール画像",
            use_container_width=True,
        )

        # 画像をダウンロード可能にする
        output_path = os.path.join(OUTPUT_DIR, "santa_profile.png")
        combined_image.save(output_path, format="PNG")

        with open(output_path, "rb") as file:
            st.download_button(
                label="画像をダウンロード",
                data=file,
                file_name="santa_profile.png",
                mime="image/png",
            )


if __name__ == "__main__":
    prepare_directories()
    main()
