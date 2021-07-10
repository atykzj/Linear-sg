import React from 'react'
import axios from 'axios';
import * as settings from '../settings';
import "./assets/Styling.css";

import CssBaseline from '@material-ui/core/CssBaseline';
import { Link } from "react-router-dom";
import { withStyles, makeStyles } from '@material-ui/core/styles';
import { Container, Grid, Paper, Typography, Slider, Button } from '@material-ui/core';


// ########################################################
// The main Home component returned by this Module
// ########################################################
function Home(props) {

    return (
        <div class="wrapper">

            <div class="text__home block">
            Ready to explore your taste and preference? Our AI will find out how your ideal house looks like in less than 5 minutes! Choose your favourite image, and we will create a mood board for you! Don't think too much.
            </div>
            <div class="btn block">
                <Link to="/quiz">
                    <Button variant="contained" color="primary">
                        Let's go!
                    </Button>
                </Link>
            </div>
        </div>
    )
}

export default Home