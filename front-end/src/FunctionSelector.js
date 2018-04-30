import React from 'react';
import List, { ListItem, ListItemSecondaryAction, ListItemText } from 'material-ui/List';
import Checkbox from 'material-ui/Checkbox';

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
        this.state = {
            checked: [0]
        };
    }

    handleToggle = value => () => {
        const { checked } = this.state;
        const currentIndex = checked.indexOf(value);
        const newChecked = [...checked];

        if (currentIndex === -1) {
            newChecked.push(value);
        } else {
            newChecked.splice(currentIndex, 1);
        }

        this.setState({checked: newChecked}, () => console.log({'check_state': this.state.checked}));
    };

    render(){
        const function_names = ['Log Compression', 'Constrast Stretch', 'Histogram Equalization', 'Reverse Video'];

        return (
            <div >
                <List>
                    {[0, 1, 2, 3].map(value => (
                        <ListItem
                            key={value}
                            role={undefined}
                            button
                            onClick={this.handleToggle(value)}
                        >
                            <Checkbox
                                checked={this.state.checked.indexOf(value) !== -1}
                                tabIndex={-1}
                                disableRipple
                            />
                            <ListItemText primary={function_names[value]} />
                            <ListItemSecondaryAction>

                            </ListItemSecondaryAction>
                        </ListItem>
                    ))}
                </List>
            </div>
        );
    }
}

export default FunctionSelector