import React from 'react';

import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import Button from '@material-ui/core/Button';

function DeviceAdd() {
  return (
    <>
      <Grid container alignItems="center">
        <Grid item sm={12}>
          <h2>Add Device</h2>
        </Grid>
      </Grid>
      <Grid>
        <h3>Information</h3>
      </Grid>
      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <TextField fullWidth variant="outlined" label="Name" />
        </Grid>
        <Grid item xs={12} md={6}>
          <TextField fullWidth variant="outlined" label="Description" />
        </Grid>
      </Grid>
      <br />
      <br />
      <Grid>
        <h3>Advance</h3>
      </Grid>
      <Grid container spacing={2}>
        <Grid item xs={12} md={4}>
          <TextField fullWidth variant="outlined" label="Address" />
        </Grid>
        <Grid item xs={12} md={4}>
          <FormControl variant="outlined" fullWidth>
            <InputLabel id="demo-simple-select-outlined-label">Warehouse</InputLabel>
            <Select labelId="demo-simple-select-outlined-label" id="demo-simple-select-outlined" label="Warehouse" fullWidth>
              <MenuItem value="phunhuan">Athi River</MenuItem>
              <MenuItem value="binhthanh">Industrial Area</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={4}>
          <FormControl variant="outlined" fullWidth>
            <InputLabel id="demo-simple-select-outlined-label">Group</InputLabel>
            <Select labelId="demo-simple-select-outlined-label" id="demo-simple-select-outlined" label="group" fullWidth>
              <MenuItem value="hcm">Environmental Monitoring</MenuItem>
              <MenuItem value="hn">Access Control</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={12} md={4}>
          <FormControl variant="outlined" fullWidth>
            <InputLabel id="demo-simple-select-outlined-label">Subgroup</InputLabel>
            <Select labelId="demo-simple-select-outlined-label" id="demo-simple-select-outlined" label="subgroup" fullWidth>
              <MenuItem value="hcm">Environmental Monitoring</MenuItem>
              <MenuItem value="hn">Access Control</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid container justify="flex-end" className="my-20">
          <Button color="primary">Add More</Button>
        </Grid>
        <br />
        <Grid container item sm={12} md={12} justify="flex-end">
          <Button variant="outlined" color="primary" className="mr-20">
            Cancel
          </Button>
          <Button color="primary" variant="contained">
            Submit
          </Button>
        </Grid>
      </Grid>
    </>
  );
}

export default DeviceAdd;
