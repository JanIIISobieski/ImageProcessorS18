import React from 'react';
import Dropzone from 'react-dropzone'
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
            all_image_array: [],
            length_array: 0,
            image_select: 0
        }
    }

    onDropSetter = (acceptedImages, rejectedImages) => {
        this.setState({accepted: acceptedImages}, () => {console.log({'accepted': this.state.accepted})});
        this.setState({rejected: rejectedImages}, () => {console.log({'rejected': this.state.rejected})});
        this.setState({all_image_array: []});
        this.setState({image_select: 0});
        acceptedImages.forEach(file => {
            const reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onloadend = () => {
                //console.log(reader.result);
                var readImage = reader.result;
                var joined = this.state.all_image_array.concat([readImage]);
                this.setState({all_image_array: joined},
                    () => {
                    this.setState({length_array: this.state.all_image_array.length},
                        () => {console.log({'length_array': this.state.length_array})});
                    console.log({'all_images': this.state.all_image_array});
                });
            };
        });
    };

    nonZeroDecrement = (val, vec_length) => {
        var decrement = val - 1;
        if (decrement === -1){
            decrement = decrement + vec_length
        }
        return decrement
    }

    onLeftButtonClick = (event) => {
        this.setState({image_select: Math.abs(this.nonZeroDecrement(this.state.image_select, this.state.length_array)) % this.state.length_array},
            () => console.log({'image_select': this.state.image_select}));
    };

    onRightButtonClick = (event) => {
        this.setState({image_select: Math.abs(this.state.image_select + 1) % this.state.length_array},
            () => console.log({'image_select': this.state.image_select}));
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
                    <Button
                        color="primary"
                        variant='raised'
                        onClick={this.onLeftButtonClick}
                        disabled={this.state.length_array === 0}
                    >
                        Previous Image
                    </Button>

                    {(this.state.image_select + 1)*(this.state.length_array > 0)} out of {this.state.length_array}

                    <Button
                        color="primary"
                        variant='raised'
                        onClick={this.onRightButtonClick}
                        disabled={this.state.length_array === 0}
                    >
                        Next Image
                    </Button>
                </div>
                <img src={this.state.all_image_array[this.state.image_select]} width='500'/>
            </section>
        );
    }
}

export default withStyles(styles)(FileUploader);