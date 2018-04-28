import React from 'react';
import Dropzone from 'react-dropzone'
import PropTypes from 'prop-types'
import { withStyles } from 'material-ui/styles'
import Button from 'material-ui/Button'

const styles = theme => ({
    button: {
        margin: theme.spacing.unit,
    },
});

class FileUploader extends React.Component {
    constructor() {
        super();
        this.state = {
            accepted: [],
            rejected: [],
            current_image_string: '',
            all_image_array: [],
            length_array: 0,
            image_select: 0
        }
    }

    onDropSetter = (acceptedImages, rejectedImages) => {
        this.setState({accepted: acceptedImages});
        this.setState({rejected: rejectedImages});
        this.setState({all_image_array: []});
        acceptedImages.forEach(file => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onloadend = () => {
                //console.log(reader.result);
                var readImage = reader.result;
                this.setState({current_image_string: readImage});
                var joined = this.state.all_image_array.concat([readImage]);
                this.setState({all_image_array: joined});
            };
            this.setState({length_array: this.state.all_image_array.length});
        });
        console.log({'accepted': this.state.accepted});
        console.log({'rejected': this.state.rejected});
        console.log({'current_image_string': this.state.current_image_string});
        console.log({'all_images': this.state.all_image_array});
        console.log({'length_array': this.state.length_array});
    };

    onRightButtonClick = (event) => {
        this.setState({image_select: (this.state.image_select + 1) % this.state.length_array});
        console.log({'image_select': this.state.image_select});
    };

    onLeftButtonClick = (event) => {
        this.setState({image_select: (this.state.image_select - 1) % this.state.length_array});
        console.log({'image_select': this.state.image_select});
    };

    render() {
        return (
            <section>
                <p>Try dropping some files here, or click to select files to upload.</p>
                <p>Only *.jpeg and *.png images will be accepted</p>
                <div className="dropzone">
                    <Dropzone
                        accept="image/jpeg, image/png"
                        onDrop= {this.onDropSetter}
                    >
                    </Dropzone>
                </div>
                <aside>
                    <h2>Accepted files</h2>
                    <ul>
                        {
                            this.state.accepted.map(f => <li key={f.name}>{f.name} - {f.size} bytes</li>)
                        }
                    </ul>
                    <h2>Rejected files</h2>
                    <ul>
                        {
                            this.state.rejected.map(f => <li key={f.name}>{f.name} - {f.size} bytes</li>)
                        }
                    </ul>
                </aside>
                <div>
                    <Button color="primary" variant='raised' onClick={this.onLeftButtonClick}>
                        Previous Image
                    </Button>

                    {this.state.image_select + 1} out of {this.state.length_array}

                    <Button color="primary" variant='raised' onClick={this.onRightButtonClick}>
                        Next Image
                    </Button>
                </div>
                <img src={this.state.all_image_array[this.state.image_select]} width='500'/>
            </section>
        );
    }
}

export default withStyles(styles)(FileUploader);