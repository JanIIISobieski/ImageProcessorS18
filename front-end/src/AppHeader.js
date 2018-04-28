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
    constructor() {
        super();
        this.state = {
          userID: '',
          badEmail: true
        };
    }

    onTextFieldChange = (event) => {
        this.setState({'userID': event.target.value});
        console.log({'UserID': this.state.userID})
    };

    validateEmail = (email) => {
        var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        var testVal = !re.test(String(email).toLowerCase());
        console.log({emailRegEx: testVal});
        return testVal
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
                            label='User E-mail'
                            defaultValue={this.state.userID}
                            onChange={this.onTextFieldChange}
                            error={this.validateEmail(this.state.userID)}>
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