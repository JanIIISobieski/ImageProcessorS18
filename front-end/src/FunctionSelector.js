import React from 'react';
import PropTypes from 'prop-types';
import { withStyles } from 'material-ui/styles';
import List, { ListItem, ListItemSecondaryAction, ListItemText } from 'material-ui/List';
import Checkbox from 'material-ui/Checkbox';
import IconButton from 'material-ui/IconButton';
import CommentIcon from '@material-ui/icons/Comment';

const styles = theme => ({
    root: {
        width: '100%',
        maxWidth: 360,
        backgroundColor: theme.palette.background.paper,
    },
});

class FunctionSelector extends React.Component {
    constructor(){
        super();
        state = {
            checked: [1, 0, 0, 0]
        };
    }

    render(){
        return (
          <div>
              What
          </div>
        );
    }
}