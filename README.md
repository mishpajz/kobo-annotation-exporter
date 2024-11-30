# Kobo annotation exporter

Used for exporting annotations from Kobo e-reader devices.

## Install

1. Install the required packages by running `pip install -r requirements.txt`.


## Usage

1. Connect your Kobo device to your computer.
2. Copy the `KoboReader.sqlite` file from the device's `/.kobo/KoboReader.sqlite` somewhere on your computer.
3. Run the script by running `python kobo-annotation-exporter.py <KoboReader>` where `<KoboReader>` is the path to the `KoboReader.sqlite` file.
4. The script will list all the books that have annotations. Enter the number of the book you want to export annotations for.
5. The script will generate a CSV file with the annotations for the specified book and save it to `output/<bookname>_annotations_.csv`.

### Recommended LLM prompt

> I'd like your help synthesizing my reading notes and annotations from [BOOK TITLE] by [AUTHOR].
> Here are my annotations and highlights from my reading:
`
`CONTENT`
`
> Please create a comprehensive summary that:
> 1. Starts with a 2-3 sentence overview of the book's core message and significance
> 2. Organizes the key insights into 3-5 major themes or sections that emerged from the content
> 3. Under each theme, provides:
>   - The most important concepts, arguments, and takeaways (5-7 bullet points per theme)
>   - Relevant examples or case studies that illustrate these points
>   - Any memorable quotes that capture the essence of this theme
> 4. Concludes with:
>   - 3-5 most actionable insights or practical applications
>   - Questions for further reflection
>   - Related books or resources for deeper exploration
> Please focus on extracting the most valuable and thought-provoking ideas rather than trying to capture everything. Feel free to combine related points and restructure the information to enhance clarity and impact.
> If you notice any key ideas from the book that aren't reflected in my annotations but are important for understanding the complete picture, please include those as well, noting them as additional context.
> Format the summary to enhance readability Aim for a length that balances comprehensiveness with conciseness (roughly equivalent to 30-40 key points across all sections).