using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CreadorEnemigos : MonoBehaviour
{
    public GameObject PrefabEnemigo;
    public float TiempoDeGeneracion = 2f;

    void CrearEnemigo() 
    {
        Instantiate(PrefabEnemigo, new Vector3(5.35f, 0f, 0f), Quaternion.identity);
    }

    public void IniciarGenerador(){InvokeRepeating("CrearEnemigo", 0f, TiempoDeGeneracion);}

    public void CancelarGeneracion(){CancelInvoke("CrearEnemigo");}
}
