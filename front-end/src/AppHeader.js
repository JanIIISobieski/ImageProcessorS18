import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import AppBar from 'material-ui/AppBar';
import Toolbar from 'material-ui/Toolbar';
import Typography from 'material-ui/Typography';
import TextField from 'material-ui/TextField';


const styles = {
    root: {
        flexGrow: 1,
    },
    flex: {
        flex: 1,
    },
    floatingLabelFocusStyle: {
        color: 'white'
    },
};


class AppHeader extends React.Component{
    constructor(props) {
        super(props);
    }

    onTextFieldChange = (event) => {
        this.props.onChange(event)
    };

    render(){
        const { classes } = this.props;
        return (
            <div className={classes.root}>
                <AppBar position="static" color='default'>
                    <Toolbar>
                        <Typography variant="title" color="inherit" className={classes.flex}>
                            Image Processor
                        </Typography>
                        <TextField
                            id='e-mail_input'
                            label='User ID'
                            defaultValue={this.props.email}
                            onChange={this.onTextFieldChange}
                            error={this.props.bad_email}
                        >
                        </TextField>
                    </Toolbar>
                </AppBar>
            </div>
        )
    }
}

AppHeader.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(AppHeader)