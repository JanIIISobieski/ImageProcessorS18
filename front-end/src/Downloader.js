import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Radio, { RadioGroup } from 'material-ui/Radio';
import { FormLabel, FormControl, FormControlLabel } from 'material-ui/Form';
import download from 'downloadjs'
import Button from 'material-ui/Button'

const styles = theme => ({
    root: {
        display: 'flex',
    },
    formControl: {
        margin: theme.spacing.unit * 1,
    },
    group: {
        margin: `${theme.spacing.unit}px 0`,
    },
});

class RadioButtonsGroup extends React.Component {
    state = {
        value: 'png',
    };

    handleChange = event => {
        this.setState({ value: event.target.value });
    };

    sendRequest = () => {
        var img = this.props.recieved.processed[0];
        var ending = this.state.value;
        var filename = 'processed';
        var mime_string = '';
        if (this.props.length === 1){
            mime_string = mime_string.concat('image/', ending);
            filename = filename.concat('.', ending)
        } else{
            mime_string = mime_string.concat('application/zip');
            filename = filename.concat('.zip')
        }
        console.log({'download': [filename, mime_string]});
        download(img, filename, mime_string);
    };

    render() {
        const { classes } = this.props;

        return (
            <div>
                <div className={classes.root}>
                    <FormControl component="fieldset" className={classes.formControl}>
                        <FormLabel component="legend">Download as:</FormLabel>
                        <RadioGroup
                            aria-label="downloader"
                            name="download_type"
                            className={classes.group}
                            value={this.state.value}
                            onChange={this.handleChange}
                        >
                            <FormControlLabel value="jpeg" control={<Radio />} label="JPEG" />
                            <FormControlLabel value="png" control={<Radio />} label="PNG" />
                            <FormControlLabel value="tiff" control={<Radio />} label="TIFF" />
                        </RadioGroup>
                    </FormControl>
                </div>
                <div>
                    <Button
                    color="primary"
                    variant='raised'
                    onClick={this.sendRequest}
                    >
                    Download
                    </Button>
                </div>
            </div>
        );
    }
}

RadioButtonsGroup.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(RadioButtonsGroup);