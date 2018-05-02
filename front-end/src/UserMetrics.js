import React from 'react';
import Table, {TableBody, TableCell, TableHead, TableRow} from 'material-ui/Table'

class UserMetrics extends React.Component{
    constructor(props) {
        super(props);
    }

    makeTable = (data) => {
        var tableArray = [];
        var upload_time = [data.up_time, '', '', ''];
        var return_time = [data.ret_time, '', '', ''];
        var user_metrics = data.user_metrics[0];
        var func_names = ['Histogram Equalization', 'Contrast Stretch', 'Log Compression', 'Reverse Video'];
        var tableArray = [];
        for (var i = 0; i < 4; i++){
            tableArray.push((
                <TableRow>
                    <TableCell>
                        {upload_time[i]}
                    </TableCell>
                    <TableCell>
                        {return_time[i]}
                    </TableCell>
                    <TableCell>
                        {func_names[i]}
                    </TableCell>
                    <TableCell>
                        {user_metrics[i]}
                    </TableCell>
                </TableRow>))
        }
        return tableArray
    };

    render() {
        var data = [];
        if (typeof this.props.data.user_metrics[0].length < 4){
            data = {
                up_time: '',
                ret_time: '',
                user_metrics: ['', '', '', '']
            }
        }   else{
            data = this.props.data
        }
        var table_body = this.makeTable(data);

        return(
            <div>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Upload Time</TableCell>
                            <TableCell>Return Time</TableCell>
                            <TableCell>Functions</TableCell>
                            <TableCell>Times Used</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            table_body
                        }
                    </TableBody>
                </Table>

            </div>
        )
    }
}

export default UserMetrics;