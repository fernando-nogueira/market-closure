import src.stocks_data as stocks
import src.index_data as index
import src.image_maker as img

def main() -> None:
    data_stocks = stocks.format_stocks_data()
    data_index = index.format_index_data()

    image = img.ImageMaker()
    image.make_image1(data_index)
    image.make_image2(data_stocks)
    image.make_image3(data_index)

if __name__ == '__main__':
    main()