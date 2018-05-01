import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import Radio, { RadioGroup } from 'material-ui/Radio';
import { FormLabel, FormControl, FormControlLabel } from 'material-ui/Form';
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
        value: 'PNG',
    };

    handleChange = event => {
        this.setState({ value: event.target.value });
    };

    sendRequest = () => {
        var img = this.props.recieved.originals[0];
        var data = img.split(',')[1];
        var url = 'data:application/octed-stream;base64,'+data;
        window.open(url);
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
                            <FormControlLabel value="JPEG" control={<Radio />} label="JPEG" />
                            <FormControlLabel value="PNG" control={<Radio />} label="PNG" />
                            <FormControlLabel value="TIFF" control={<Radio />} label="TIFF" />
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