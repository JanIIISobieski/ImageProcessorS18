import React from 'react';
import List, { ListItem, ListItemSecondaryAction, ListItemText } from 'material-ui/List';
import Checkbox from 'material-ui/Checkbox';
import Button from 'material-ui/Button'

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

    sendRequest = () => {

    };

    render(){
        const function_names = ['Log Compression', 'Contrast Stretch', 'Histogram Equalization', 'Reverse Video'];

        return (
            <div >
                <List
                    disablePadding={true}
                >
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
                <Button
                    color="primary"
                    variant='raised'
                    onClick={this.sendRequest}
                    disabled={this.state.checked.length === 0}
                >
                    Process Images
                </Button>
            </div>
        );
    }
}

export default FunctionSelector