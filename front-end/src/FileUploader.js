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
            image_select: 0,
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
            () => {
                console.log({'image_select': this.state.image_select});
            });
    };

    onRightButtonClick = (event) => {
        this.setState({image_select: Math.abs(this.state.image_select + 1) % this.props.length},
            () => {
                console.log({'image_select': this.state.image_select})
                console.log({'image_selector': this.selectIndex()});
            });
    };

    selectIndex = () => {
        var index = 0;
        console.log({'boolean_process': this.props.processed_data.functions === ''});
        if (this.props.processed_data.functions === ''){
            index = 0;
        } else {
            index = this.state.image_select;
        }
        return index
    };

    writeImageSize = () => {
        var size = ['', ''];
        if (this.props.processed_data.functions === '') {
            size = ['', '']
        } else {
            size = this.props.processed_data.size[this.state.image_select]
        }
        return size
    };

    render() {
        return (
            <div>
            <section>
                <div className="center">
                    <Dropzone
                        accept="image/jpeg, image/png, .zip"
                        onDrop= {this.onDrop}
                    >
                        Drag .png, .jpeg, or .zip files of images here
                    </Dropzone>
                </div>
                <div className='center'>
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
                    <div className='center'>
                        Image size: {this.writeImageSize()[0]}
                        x {this.writeImageSize()[1]}
                    </div>
                </div>
            </section>
                <div className='image_adjacent'>
                    <img src={this.props.all_image_array[this.state.image_select]}/>
                    <img src={this.props.processed_data.processed[this.selectIndex]}/>
                </div>
                <div className='image_adjacent'>
                    <img src={this.props.processed_data.o_hist[this.selectIndex]}/>
                    <img src={this.props.processed_data.p_hist[this.selectIndex]}/>
                </div>
            </div>
        );
    }
}

export default withStyles(styles)(FileUploader);