import React, { useState, useEffect } from 'react';
import { Grid, Paper, TextField, Button } from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import Avatar from '@material-ui/core/Avatar';
import img from '../assets/images/User2.png';
import { axiosInstance, axiosInstanceGet } from '../helpers/ApiFunctions';

const useStyles = makeStyles({
  root: {
    maxWidth: 1200,
    margin: 'auto',
  },
  card: {
    maxWidth: 800,
    margin: 'auto',
  },
  media: {
    maxHeight: 45,
  },
  form: {
    maxWidth: 800,
    backgroundColor: '#F5F5F5',
    margin: 'auto',
  },
});

const OverviewPage = ({ title, description, id }) => {
  const [exerciseFeedback] = useState([]);
  const [formDataSet, setFormDataSet] = useState({ sets: id });
  const classes = useStyles();

  function createFeedbackList(feedbacks) {
    Object.entries(feedbacks).forEach(([comment]) => {
      if (feedbacks[comment].sets === Number(id)) {
        exerciseFeedback.push(feedbacks[comment]);
      }
    });
  }

  function getFeedback() {
    axiosInstanceGet
      .get(`/feedback/`)
      .then((response) => {
        createFeedbackList(response.data);
      })
      .catch((e) => {
        return e;
      });
  }

  function onsubmitPostComment() {
    axiosInstance
      .post('/feedback/', formDataSet)
      .then(() => {
        getFeedback();
      })
      .catch((e) => {
        return e;
      });
  }

  useEffect(() => {
    getFeedback();
  }, []);

  console.log(exerciseFeedback);

  return (
    <Paper className={classes.root}>
      <Grid>
        <h1>{title}</h1>
        <h2>{description}</h2>
      </Grid>
      <Grid className={classes.form}>
        <h2>Legg igjen en kommentar!</h2>
        <div>
          <TextField
            name="owner"
            rowsMax={1}
            required
            placeholder="Navn"
            variant="outlined"
            onChange={
              (e) =>
                setFormDataSet({
                  ...formDataSet,
                  owner: e.target.value,
                })
              // eslint-disable-next-line react/jsx-curly-newline
            }
          />
        </div>
        <div>
          <TextField
            name="comment"
            multiline="true"
            rowsMax={50}
            required
            placeholder="Kommentar..."
            variant="outlined"
            onChange={
              (e) =>
                setFormDataSet({
                  ...formDataSet,
                  comment: e.target.value,
                })
              // eslint-disable-next-line react/jsx-curly-newline
            }
          />
        </div>
        <Button
          variant="contained"
          color="secondary"
          onClick={() => onsubmitPostComment()}
        >
          Send inn
        </Button>
      </Grid>
      <Grid className={classes.card}>
        <h2>Kommentarer...</h2>
        <Card>
          <Avatar alt="placeholder_icon" src={img} />
          <CardContent>
            <Typography gutterBottom variant="h5" component="h2">
              Tittel
            </Typography>
            <Typography variant="body2" color="textSecondary" component="p">
              Lizards are a widespread group of squamate reptiles, with over
              6,000 species, ranging across all continents except Antarctica
            </Typography>
          </CardContent>
        </Card>
      </Grid>
    </Paper>
  );
};

export default OverviewPage;
