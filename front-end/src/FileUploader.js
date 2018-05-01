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
    constructor(props) {
        super(props);
        this.state = {
            image_select: 0
        }
    }

    onDrop = (acceptedImages, rejectedImages) => {
        this.props.onDrop(acceptedImages, rejectedImages)
    };

    nonZeroDecrement = (val, vec_length) => {
        var decrement = val - 1;
        if (decrement === -1){
            decrement = decrement + vec_length
        }
        return decrement
    };

    onLeftButtonClick = (event) => {
        this.setState({image_select: Math.abs(
            this.nonZeroDecrement(this.state.image_select, this.props.length)) % this.props.length},
            () => console.log({'image_select': this.state.image_select}));
    };

    onRightButtonClick = (event) => {
        this.setState({image_select: Math.abs(this.state.image_select + 1) % this.props.length},
            () => console.log({'image_select': this.state.image_select}));
    };

    render() {
        return (
            <div>
            <section>
                <div className="dropzone">
                    <Dropzone
                        accept="image/jpeg, image/png, .zip"
                        onDrop= {this.onDrop}
                    >
                    </Dropzone>
                </div>
                <div>
                    <Button
                        color="primary"
                        variant='raised'
                        onClick={this.onLeftButtonClick}
                        disabled={this.props.length === 0}
                    >
                        Previous Image
                    </Button>

                    {(this.state.image_select + 1)*(this.props.length > 0)} out of {this.props.length}

                    <Button
                        color="primary"
                        variant='raised'
                        onClick={this.onRightButtonClick}
                        disabled={this.props.length === 0}
                    >
                        Next Image
                    </Button>
                </div>
            </section>
                <div className='image_adjacent'>
                    <img src={this.props.all_image_array[this.state.image_select]}/>
                    <img src={this.props.processed_data.originals[this.state.image_select]}/>
                </div>
            </div>
        );
    }
}

export default withStyles(styles)(FileUploader);