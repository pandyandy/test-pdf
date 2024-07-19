import streamlit as st
import markdown2
import pdfkit
import base64
from pathlib import Path

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    return b64_string

current_dir = Path(__file__).parent
image_path = current_dir / 'static' / 'logo.png'
image_base64 = get_image_base64(image_path)

markdown_content = f"""
## Environment Initialization Instructions

### Github Repository Initialization

1. **Download** the generated Github Actions zip file using the button above.
2. **Create and pull** the github repository.
3. **Unpack** the `git_actions.zip` in the repository root folder:
    1. This will create a `.github/actions` folder, overwrite it if it exists.
4. **Run** the following commands:
    1. `git add .`
    2. `git commit -m "Initial commit"`
    3. `git push`
5. **Create** long-lived git branches for your environment (aside from the main one):
    1. E.g. `git checkout -b DEV`
6. **Commit and push** to each created branch:
    1. This step may be skipped if you perform KBC PULL first on the main branch and then create branches in the Github repository off that one.

7. In the repository [settings](https://github.com/your-repository/settings), **create the following environments**:
    - PRD
    - DEV

<p align="center">
    <img src="data:image/png;base64,{image_base64}" alt="Keboola Logo" width="300">
</p>

8. You may set the **ENV restrictions**:
    - Note that the github actions need access to both related environments (DEV/PROD) in order to perform comparison validations.

9. For each environment set the following:
    - (Detailed instructions for each environment should be provided here)
"""
st.markdown(markdown_content, unsafe_allow_html=True)

def create_pdf(html):
    pdfkit.from_string(html, 'output.pdf')
    with open('output.pdf', 'rb') as f:
        return f.read()

if st.button('Convert to PDF'):
    html_content = markdown2.markdown(markdown_content)
    pdf = create_pdf(html_content)
    st.download_button('Download PDF', data=pdf, file_name='instructions.pdf', mime='application/pdf')