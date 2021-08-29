using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class RecivePosition : MonoBehaviour
{
    public OSC osc;
    public Transform[] allChildren;

    // Use this for initialization
    void Start()
    {
        allChildren = GetComponentsInChildren<Transform>();
        osc.SetAddressHandler("/VMT/Room/Unity", OnReceiveMsg);
    }

    // Update is called once per frame
    void Update()
    {

    }

    void OnReceiveMsg(OscMessage message)
    {
        string index = message.GetInt(0).ToString();
        float px = message.GetFloat(3);
        float py = message.GetFloat(4);
        float pz = message.GetFloat(5);
        float qx = message.GetFloat(6);
        float qy = message.GetFloat(7);
        float qz = message.GetFloat(8);
        float qw = message.GetFloat(9); 

        SetBodyPosition(index, px, py, pz, qx, qy, qz, qw);
    }

    void SetBodyPosition(string bodyName, float px, float py, float pz, float qx, float qy, float qz, float qw)
    {
        Quaternion quaternion = (qx, qy, qz, qw);
        foreach (Transform child in allChildren)
        {
            if (child.gameObject.name == bodyName)
            {
                child.position = new Vector3(px, py, pz);
                child.rotation = ConvertToUnity(quaternion);
            }
        }
    }

    Quaternion ConvertToUnity(Quaternion input)
    {
        return new Quaternion(
            input.y,
            -input.z,
            -input.x,
            input.w
        );
    }
}